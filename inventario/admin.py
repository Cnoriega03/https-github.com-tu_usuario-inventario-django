from django.contrib import admin

from .models import Categoria, MovimientoInventario, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "categoria",
        "stock_actual",
        "stock_minimo",
        "precio_compra",
        "precio_venta",
        "fecha_registro",
        "esta_bajo_minimo",
    )
    list_filter = ("categoria",)
    search_fields = ("codigo", "nombre", "descripcion")
    readonly_fields = ("fecha_registro",)

    @admin.display(boolean=True, description="Bajo minimo")
    def esta_bajo_minimo(self, obj):
        return obj.bajo_stock_minimo


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "tipo", "cantidad", "fecha", "observacion")
    list_filter = ("tipo", "fecha")
    search_fields = ("producto__codigo", "producto__nombre", "observacion")
    readonly_fields = ("fecha",)
