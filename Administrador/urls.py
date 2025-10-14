from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('dashboard/',views.Dasboard_view,name='dashboard'),
    path('usuarios/',views.Usuarios_view,name='usuarios'),
    path('toggle-user-status/<int:user_id>/<str:user_type>/<str:action>/', csrf_exempt(views.toggle_user_status), name='toggle_user_status'),
    path('update-user/', csrf_exempt(views.update_user), name='update_user'),
    path('csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('Productos/',views.Armarios_view,name='Gproductos'),
    path('GestionarProductos/',views.GestionarProductos_view,name='GestionarProductos'),
    path('Productos/',views.Sillas_view,name='Gproductos'),
    path('agregar_producto/', views.agregar_producto_view, name='agregar_producto'),
    path('editar_producto/<int:producto_id>/', views.editar_producto_view, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto_view, name='eliminar_producto'),
    path('admin/', admin.site.urls),
]
