from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboardEmpresa/',views.Dasboard_view,name='dashboardEmpresa'),
    path('GestiProductos/',views.GestionarProductos_view,name='GestiProductos'),
]
