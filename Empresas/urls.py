from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/',views.Dasboard_view,name='dashboard'),
    path('GestiProductos/',views.GestionarProductos_view,name='GestiProductos'),
]
