# Generated manually for the initial inventory schema.
from decimal import Decimal

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("descripcion", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "categoria",
                "verbose_name_plural": "categorias",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="Producto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=50, unique=True)),
                ("nombre", models.CharField(max_length=150)),
                ("descripcion", models.TextField(blank=True)),
                ("stock_actual", models.PositiveIntegerField(default=0)),
                ("stock_minimo", models.PositiveIntegerField(default=0)),
                ("precio_compra", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=10)),
                ("precio_venta", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=10)),
                ("fecha_registro", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="productos",
                        to="inventario.categoria",
                    ),
                ),
            ],
            options={
                "ordering": ["nombre"],
                "permissions": [("puede_ver_alertas", "Puede ver alertas de stock minimo")],
            },
        ),
        migrations.CreateModel(
            name="MovimientoInventario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("ENTRADA", "Entrada"), ("SALIDA", "Salida")], max_length=10)),
                ("cantidad", models.PositiveIntegerField()),
                ("fecha", models.DateTimeField(default=django.utils.timezone.now)),
                ("observacion", models.TextField(blank=True)),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movimientos",
                        to="inventario.producto",
                    ),
                ),
            ],
            options={
                "verbose_name": "movimiento de inventario",
                "verbose_name_plural": "movimientos de inventario",
                "ordering": ["-fecha"],
            },
        ),
    ]
