from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    fecha_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["nombre"]
        permissions = [
            ("puede_ver_alertas", "Puede ver alertas de stock minimo"),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def bajo_stock_minimo(self):
        return self.stock_actual < self.stock_minimo


class MovimientoInventario(models.Model):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"

    TIPO_CHOICES = [
        (ENTRADA, "Entrada"),
        (SALIDA, "Salida"),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="movimientos",
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    observacion = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "movimiento de inventario"
        verbose_name_plural = "movimientos de inventario"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto} ({self.cantidad})"

    def efecto_en_stock(self):
        if self.tipo == self.ENTRADA:
            return self.cantidad
        return -self.cantidad

    def clean(self):
        if not self.cantidad or self.cantidad <= 0:
            raise ValidationError({"cantidad": "La cantidad debe ser mayor que cero."})

        stock_disponible = self.producto.stock_actual

        if self.pk:
            movimiento_anterior = MovimientoInventario.objects.select_related("producto").get(pk=self.pk)

            if movimiento_anterior.producto_id == self.producto_id:
                stock_disponible -= movimiento_anterior.efecto_en_stock()
            else:
                stock_origen = movimiento_anterior.producto.stock_actual - movimiento_anterior.efecto_en_stock()
                if stock_origen < 0:
                    raise ValidationError(
                        "No se puede modificar este movimiento porque dejaria stock negativo en el producto anterior."
                    )

        if self.tipo == self.SALIDA and self.cantidad > stock_disponible:
            raise ValidationError({"cantidad": "No hay stock suficiente para registrar esta salida."})

    def save(self, *args, **kwargs):
        self.full_clean()

        with transaction.atomic():
            if self.pk:
                movimiento_anterior = MovimientoInventario.objects.select_for_update().get(pk=self.pk)
                producto_anterior = Producto.objects.select_for_update().get(pk=movimiento_anterior.producto_id)
                producto_anterior.stock_actual -= movimiento_anterior.efecto_en_stock()

                if producto_anterior.stock_actual < 0:
                    raise ValidationError(
                        "No se puede modificar este movimiento porque dejaria stock negativo."
                    )

                producto_anterior.save(update_fields=["stock_actual"])

            super().save(*args, **kwargs)

            producto = Producto.objects.select_for_update().get(pk=self.producto_id)
            producto.stock_actual += self.efecto_en_stock()

            if producto.stock_actual < 0:
                raise ValidationError("El stock no puede quedar en negativo.")

            producto.save(update_fields=["stock_actual"])

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            producto = Producto.objects.select_for_update().get(pk=self.producto_id)
            producto.stock_actual -= self.efecto_en_stock()

            if producto.stock_actual < 0:
                raise ValidationError(
                    "No se puede eliminar este movimiento porque dejaria stock negativo."
                )

            producto.save(update_fields=["stock_actual"])
            super().delete(*args, **kwargs)
