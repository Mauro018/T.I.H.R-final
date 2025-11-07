from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Login_view, name='login'),
    path('', views.LoginAdmin_view, name='loginAdmin'),
    path('', views.chatbot, name="chatbot"),
    path('registro', views.registro, name='registro'),
    path('logout', views.Logout_view, name='logout'),
    path('home3', views.Home3_view, name='home3'),
    path('contactenos', views.contactenos, name='contactenos'),
    path('reglas', views.reglas, name='reglas'),
    path('idea', views.ideas_view, name='idea'),
    path('empresa/ideas', views.empresa_ideas_view, name='empresa_ideas'),
    path('carrito', views.carrito, name='carrito'),
    path ('MetodosPago', views.MetodosPago, name='MetodosPago'),
    # URLs para comentarios
    path('comentarios/', views.comentarios_view, name='comentarios'),
    path('comentarios/crear/', views.crear_comentario_view, name='crear_comentario'),
    path('comentarios/eliminar/<int:comentario_id>/', views.eliminar_comentario_view, name='eliminar_comentario'),
    # URLs para perfil de usuario
    path('perfil/', views.perfil_usuario_view, name='perfilUsuario'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    path('',include('Productos.urls')),
    path('',include('Administrador.urls')),
    path('',include('Empresas.urls')),
]