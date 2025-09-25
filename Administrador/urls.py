from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('dashboard/',views.Dasboard_view,name='dashboard'),
    path('usuarios/',views.Usuarios_view,name='usuarios'),
    path('GestionarUsuarios/',views.GestionarUsuarios_view,name='GestionarUsuarios'),
    path('Productos/',views.Armarios_view,name='Gproductos'),
    path('GestionarProductos/',views.GestionarProductos_view,name='GestionarProductos'),
    path('Productos/',views.Sillas_view,name='Gproductos'),
    path('agregar_producto/', views.agregar_producto_view, name='agregar_producto'),
    path('editar_producto/<int:producto_id>/', views.editar_producto_view, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto_view, name='eliminar_producto'),
    path('admin/', admin.site.urls),
]
