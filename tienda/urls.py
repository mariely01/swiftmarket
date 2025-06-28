from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('comentar/', views.comentar, name='comentar'),
    path('checkout/', views.checkout, name='checkout'),
    path('historial_compras/', views.historial_compras, name='historial_compras'),
    path('compra_confirmada/<int:compra_id>/', views.compra_confirmada, name='compra_confirmada'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
]