from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, MovimientoInventarioForm, ProductoForm
from .models import Categoria, MovimientoInventario, Producto


@login_required
def dashboard(request):
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_stock = Producto.objects.aggregate(total=Sum("stock_actual"))["total"] or 0
    productos_bajo_minimo = Producto.objects.filter(stock_actual__lt=F("stock_minimo")).count()
    alertas_stock = Producto.objects.select_related("categoria").filter(
        stock_actual__lt=F("stock_minimo")
    )[:8]
    ultimos_movimientos = MovimientoInventario.objects.select_related("producto")[:8]

    context = {
        "total_productos": total_productos,
        "total_categorias": total_categorias,
        "total_stock": total_stock,
        "productos_bajo_minimo": productos_bajo_minimo,
        "alertas_stock": alertas_stock,
        "ultimos_movimientos": ultimos_movimientos,
    }
    return render(request, "inventario/dashboard.html", context)


@login_required
@permission_required("inventario.view_categoria", raise_exception=True)
def categoria_lista(request):
    consulta = request.GET.get("q", "").strip()
    categorias = Categoria.objects.all()

    if consulta:
        categorias = categorias.filter(
            Q(nombre__icontains=consulta) | Q(descripcion__icontains=consulta)
        )

    return render(
        request,
        "inventario/categoria_lista.html",
        {"categorias": categorias, "consulta": consulta},
    )


@login_required
@permission_required("inventario.add_categoria", raise_exception=True)
def categoria_crear(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria registrada correctamente.")
            return redirect("categoria_lista")
    else:
        form = CategoriaForm()

    return render(request, "inventario/categoria_form.html", {"form": form, "titulo": "Nueva categoria"})


@login_required
@permission_required("inventario.change_categoria", raise_exception=True)
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria actualizada correctamente.")
            return redirect("categoria_lista")
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, "inventario/categoria_form.html", {"form": form, "titulo": "Editar categoria"})


@login_required
@permission_required("inventario.view_producto", raise_exception=True)
def producto_lista(request):
    consulta = request.GET.get("q", "").strip()
    productos = Producto.objects.select_related("categoria")

    if consulta:
        productos = productos.filter(
            Q(codigo__icontains=consulta)
            | Q(nombre__icontains=consulta)
            | Q(descripcion__icontains=consulta)
            | Q(categoria__nombre__icontains=consulta)
        )

    return render(
        request,
        "inventario/producto_lista.html",
        {"productos": productos, "consulta": consulta},
    )


@login_required
@permission_required("inventario.add_producto", raise_exception=True)
def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto registrado correctamente.")
            return redirect("producto_lista")
    else:
        form = ProductoForm()

    return render(request, "inventario/producto_form.html", {"form": form, "titulo": "Nuevo producto"})


@login_required
@permission_required("inventario.change_producto", raise_exception=True)
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("producto_lista")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "inventario/producto_form.html", {"form": form, "titulo": "Editar producto"})


@login_required
@permission_required("inventario.add_movimientoinventario", raise_exception=True)
def registrar_entrada(request):
    return _registrar_movimiento(request, MovimientoInventario.ENTRADA, "Registrar entrada de stock")


@login_required
@permission_required("inventario.add_movimientoinventario", raise_exception=True)
def registrar_salida(request):
    return _registrar_movimiento(request, MovimientoInventario.SALIDA, "Registrar salida de stock")


def _registrar_movimiento(request, tipo, titulo):
    if request.method == "POST":
        form = MovimientoInventarioForm(request.POST, tipo=tipo)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Movimiento registrado y stock actualizado.")
                return redirect("producto_lista")
            except ValidationError as exc:
                form.add_error(None, exc)
    else:
        form = MovimientoInventarioForm(tipo=tipo)

    return render(request, "inventario/movimiento_form.html", {"form": form, "titulo": titulo})


@login_required
@permission_required("inventario.view_movimientoinventario", raise_exception=True)
def movimiento_lista(request):
    movimientos = MovimientoInventario.objects.select_related("producto")
    return render(request, "inventario/movimiento_lista.html", {"movimientos": movimientos})
