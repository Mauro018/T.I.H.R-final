from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboardEmpresa/',views.Dasboard_view,name='dashboardEmpresa'),
    path('GestiProductos/',views.GestionarProductos_view,name='GestiProductos'),
    path('ArmariosP/',views.Armarios_view2,name='GestiProductos'),
    path('agregar_producto2/', views.agregar_producto_view2, name='agregar_producto2'),
    path('editar_producto2/<int:producto_id>/', views.editar_producto_view2, name='editar_producto2'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto_view2, name='eliminar_producto2'),
]
