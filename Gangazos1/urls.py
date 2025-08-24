"""
URL configuration for Gangazos1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from core import views

urlpatterns = [
    path('',views.home,name='home'),
    path('', views.chatbot, name="chatbot"),
    path('about/',views.about,name='about'),
    path('portafolio/',views.portafolio,name='portafolio'),
    path('contact/',views.contact,name='contact'),
    path('reglas/',views.reglas,name='reglas'),
    path('productos2/',views.productos2,name='productos2'),
    path('contactenos/',views.contactenos,name='contactenos'),
    path('productos/',views.productos,name='productos'),
    path('registro/',views.registro,name='registro'),
    path('login/',views.Login_view,name='login'),
    path('loginAdmin/',views.LoginAdmin_view,name='loginAdmin'),
    path('logout/',views.Logout_view,name='logout'),
    path('home2/',views.Home2_view,name='home2'),
    path('home3/',views.Home3_view,name='home3'),
    path('idea/',views.idea,name='idea'),
    path('carrito', views.carrito, name='carrito'),
    path('MetodosPago', views.MetodosPago, name='MetodosPago'),
    path('',include('Productos.urls')),
    path('',include('Administrador.urls')),
    path('admin/', admin.site.urls),
]
