from django import forms

from .models import Categoria, MovimientoInventario, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_clases_bootstrap(self)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "codigo",
            "nombre",
            "descripcion",
            "categoria",
            "stock_actual",
            "stock_minimo",
            "precio_compra",
            "precio_venta",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_clases_bootstrap(self)


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["producto", "cantidad", "observacion"]
        widgets = {
            "observacion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, tipo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = tipo
        self.fields["producto"].queryset = Producto.objects.order_by("nombre")
        aplicar_clases_bootstrap(self)

    def save(self, commit=True):
        movimiento = super().save(commit=False)
        movimiento.tipo = self.tipo
        if commit:
            movimiento.save()
        return movimiento


def aplicar_clases_bootstrap(form):
    for field in form.fields.values():
        css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
        field.widget.attrs["class"] = css_class
