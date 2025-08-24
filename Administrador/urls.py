from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/',views.Dasboard_view,name='dashboard'),
    path('usuarios/',views.Usuarios_view,name='usuarios'),
    path('GestionarUsuarios/',views.GestionarUsuarios_view,name='GestionarUsuarios'),
    path('Productos/',views.Armarios_view,name='Gproductos'),
    path('GestionarProductos/',views.GestionarProductos_view,name='GestionarProductos'),
]
