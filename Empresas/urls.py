from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('dashboardEmpresa/',views.Dasboard_view,name='dashboardEmpresa'),
    path('GestiProductos/',views.GestionarProductos_view,name='GestiProductos'),
    path('agregar_producto2/', views.agregar_producto_view2, name='agregar_producto2'),
    path('editar_producto2/<str:categoria>/<int:producto_id>/', views.editar_producto_view2, name='editar_producto2'),
    path('eliminar_producto/<str:categoria>/<int:producto_id>/', views.eliminar_producto_view2, name='eliminar_producto2'),
    path("ideas/", views.empresa_ideas_view, name="empresa_ideas"),
    path("idea/imagen/<int:idea_id>/", views.ver_imagen_idea, name="ver_imagen_idea"),
    path("idea/modelo3d/<int:idea_id>/", views.ver_modelo_3d_idea, name="ver_modelo_3d_idea"),
    path('usuarios/', views.usuarios_view, name='usuarios'),
    path('toggle-user-status/<int:user_id>/<str:user_type>/<str:action>/', csrf_exempt(views.toggle_user_status), name='toggle_user_status'),
    path('update-user/', csrf_exempt(views.update_user), name='update_user'),
    path('csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('gestion-pagos/', views.gestion_pagos_view, name='gestion_pagos'),
    path('confirmar-pago/<int:pago_id>/', csrf_exempt(views.confirmar_pago_view), name='confirmar_pago'),
    path('rechazar-pago/<int:pago_id>/', csrf_exempt(views.rechazar_pago_view), name='rechazar_pago'),
    path('gestion-pedidos/', views.gestion_pedidos_view, name='gestion_pedidos'),
    path('actualizar-estado-pedido/<int:pedido_id>/', csrf_exempt(views.actualizar_estado_pedido_view), name='actualizar_estado_pedido'),
    path('estadisticas/', views.estadisticas_view, name='estadisticas'),
    path('inventario/', views.inventario_view, name='inventario'),
    path('actualizar-inventario/', csrf_exempt(views.actualizar_inventario_view), name='actualizar_inventario'),
]