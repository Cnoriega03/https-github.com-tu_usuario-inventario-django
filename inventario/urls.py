from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("categorias/", views.categoria_lista, name="categoria_lista"),
    path("categorias/nueva/", views.categoria_crear, name="categoria_crear"),
    path("categorias/<int:pk>/editar/", views.categoria_editar, name="categoria_editar"),
    path("productos/", views.producto_lista, name="producto_lista"),
    path("productos/nuevo/", views.producto_crear, name="producto_crear"),
    path("productos/<int:pk>/editar/", views.producto_editar, name="producto_editar"),
    path("stock/entrada/", views.registrar_entrada, name="registrar_entrada"),
    path("stock/salida/", views.registrar_salida, name="registrar_salida"),
    path("movimientos/", views.movimiento_lista, name="movimiento_lista"),
]
