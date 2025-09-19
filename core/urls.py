from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Login_view, name='login'),
    path('', views.LoginAdmin_view, name='loginAdmin'),
    path('', views.chatbot, name="chatbot"),
    path('registro', views.registro, name='registro'),
    path('logout', views.Logout_view, name='logout'),
    path('home2', views.Home2_view, name='home2'),
    path('home3', views.Home3_view, name='home3'),
    path('productos2', views.productos2, name='productos2'),
    path('contactenos', views.contactenos, name='contactenos'),
    path('reglas', views.reglas, name='reglas'),
    path('idea', views.idea, name='idea'),
    path('carrito', views.carrito, name='carrito'),
    path ('MetodosPago', views.MetodosPago, name='MetodosPago'),
    path('',include('Productos.urls')),
    path('',include('Administrador.urls')),
    path('',include('Empresas.urls')),
]