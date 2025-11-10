from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, AgregarForm, LoginFormEmpresa, IdeaForm
from .models import UserClientes, Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios, UserEmpresa, Idea, Pago, Pedido, Comentario
from .logic import obtener_respuesta
import json

html_base = """
<h1>Gangazos</h1>
<ul>
    <li><a href="/">Inicio</a></li>
    <li><a href="/about">Sobre los Gangazos</a></li>
    <li><a href="/portafolio">Categorias en oferta</a></li>
    <li><a href="/contact">Contactenos</a></li>
    <li><a href="/productos">Productos</a></li>
    <li><a href="/login">Iniciar sesión</a></li>
    <li><a href="/logout">Cerrar sesión</a></li>
</ul>
"""

# Create your views here.
def home(request):
    from django.db.models import Case, When, IntegerField
    
    # Obtener comentarios aprobados primero, luego otros estados, limitado a 10
    comentarios = Comentario.objects.annotate(
        orden_estado=Case(
            When(estado='aprobado', then=1),
            When(estado='rechazado', then=3),
            When(estado='pendiente', then=2),
            output_field=IntegerField(),
        )
    ).order_by('orden_estado', '-fecha_aprobacion', '-fecha_creacion')[:10]
    
    context = {
        'comentarios': comentarios,
    }
    return render(request, "core/home.html", context)

def about(request):
    return render(request,"core/about.html")

def portafolio(request):
    return render(request,"core/portafolio.html")

def productos(request):
    # Obtener el usuario de la sesión
    usernameCliente = request.session.get('usernameCliente')
    usuario = None
    if usernameCliente:
        try:
            usuario = UserClientes.objects.get(usernameCliente=usernameCliente)
        except UserClientes.DoesNotExist:
            pass
    
    # Obtener todos los productos de la base de datos (límite de 10 para el carrusel)
    mesas = Mesas.objects.all()[:10]
    sillas = Sillas.objects.all()[:10]
    armarios = Armarios.objects.all()[:10]
    cajoneras = Cajoneras.objects.all()[:10]
    escritorios = Escritorios.objects.all()[:10]
    utensilios = Utensilios.objects.all()[:10]
    
    context = {
        'usuario': usuario,
        'mesas': mesas,
        'sillas': sillas,
        'armarios': armarios,
        'cajoneras': cajoneras,
        'escritorios': escritorios,
        'utensilios': utensilios,
    }
    
    return render(request, 'core/productos.html', context)

def contact(request):
    # Obtener el usuario de la sesión
    usernameCliente = request.session.get('usernameCliente')
    usuario = None
    if usernameCliente:
        try:
            usuario = UserClientes.objects.get(usernameCliente=usernameCliente)
        except UserClientes.DoesNotExist:
            pass
    return render(request, 'core/contact.html', {'usuario': usuario})

def Login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usernameCliente = form.cleaned_data['usernameCliente']
            passwordCliente = form.cleaned_data['passwordCliente']
            try:
                user = UserClientes.objects.get(usernameCliente=usernameCliente, passwordCliente=passwordCliente)
                # Guardar el usuario en la sesión
                request.session['usernameCliente'] = usernameCliente
                request.session.modified = True
                return redirect('productos')
            except UserClientes.DoesNotExist:
                error_message = "Usuario o contraseña incorrectos"
                return render(request, 'core/login.html', {'error_message': error_message})
    else:
        form = LoginForm()
    return render(request,'core/login.html', {'form': form})

def LoginEmpresa_view(request):
    if request.method == 'POST':
        form = LoginFormEmpresa(request.POST)
        if form.is_valid():
            usernameEmpresa = form.cleaned_data['usernameEmpresa']
            passwordEmpresa = form.cleaned_data['passwordEmpresa']
            try:
                userEmpresa = UserEmpresa.objects.get(usernameEmpresa=usernameEmpresa, passwordEmpresa=passwordEmpresa)
                # Guardar información de la empresa en la sesión
                request.session['usernameEmpresa'] = userEmpresa.usernameEmpresa
                request.session['empresa_id'] = userEmpresa.id
                request.session.modified = True
                return redirect('dashboardEmpresa')
            except UserEmpresa.DoesNotExist:
                error_message = "Usuario o contraseña incorrectos"
                return render(request, 'core/loginEmpresa.html', {'error_message': error_message})
    else:
        form = LoginFormEmpresa()
    return render(request,'core/loginEmpresa.html', {'form': form})

def Logout_view(request):
    # Limpiar datos específicos de la sesión
    request.session.pop('usernameEmpresa', None)
    request.session.pop('empresa_id', None)
    # Limpiar toda la sesión
    logout(request)
    return redirect('home')

def Home2_view(request):
    return render(request,'core/home2.html')

def Home3_view(request):
    # Obtener el usuario de la sesión
    usernameCliente = request.session.get('usernameCliente')
    usuario = None
    if usernameCliente:
        try:
            usuario = UserClientes.objects.get(usernameCliente=usernameCliente)
        except UserClientes.DoesNotExist:
            pass
    return render(request, 'core/home3.html', {'usuario': usuario})

def registro(request):
    if request.method =="POST":
        form = AgregarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AgregarForm()
    context={'form':form}
    return render(request,'core/registro.html', context)

def productos2(request):
    return render(request,"core/productos2.html")

def contactenos(request):
    return render(request,"core/contactenos.html")

def reglas(request):
    return render(request,"core/reglas.html")

def idea(request):
    # Obtener el usuario de la sesión
    usernameCliente = request.session.get('usernameCliente')
    usuario = None
    if usernameCliente:
        try:
            usuario = UserClientes.objects.get(usernameCliente=usernameCliente)
        except UserClientes.DoesNotExist:
            pass
    return render(request, 'core/idea.html', {'usuario': usuario})

def carrito(request):
    # Obtener el usuario de la sesión
    usernameCliente = request.session.get('usernameCliente')
    usuario = None
    if usernameCliente:
        try:
            usuario = UserClientes.objects.get(usernameCliente=usernameCliente)
        except UserClientes.DoesNotExist:
            pass
    return render(request, 'core/carrito.html', {'usuario': usuario})

def MetodosPago(request):
    return render(request,"core/MetodosPago.html")

def chatbot(request):
    # Inicializa el historial del chat en la sesión si no existe
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
        # Añade un mensaje de bienvenida inicial del bot solo la primera vez
        request.session['chat_history'].append({"sender": "bot", "message": "¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?"})

    if request.method == "POST":
        mensaje_usuario = request.POST.get("mensaje", "").strip()
        if mensaje_usuario:
            # Añade el mensaje del usuario al historial
            request.session['chat_history'].append({"sender": "user", "message": mensaje_usuario})
            
            # Obtiene la respuesta del bot
            respuesta_bot = obtener_respuesta(mensaje_usuario)
            
            # Añade la respuesta del bot al historial
            request.session['chat_history'].append({"sender": "bot", "message": respuesta_bot})
            
            # Marca la sesión como modificada para asegurar que Django la guarde
            request.session.modified = True

    # Pasa el historial completo a la plantilla
    return render(request, "chatbot.html", {"chat_history": request.session['chat_history']})

def ideas_view(request):
    """
    Maneja la creación y visualización de ideas usando ModelForm.
    """
    # Obtener el usuario de la sesión
    usernameCliente = request.session.get('usernameCliente')
    usuario = None
    if usernameCliente:
        try:
            usuario = UserClientes.objects.get(usernameCliente=usernameCliente)
        except UserClientes.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar sin commit para agregar el autor
            idea = form.save(commit=False)
            # Asignar automáticamente el nombre del usuario de la sesión
            if usuario:
                idea.autor = usuario.usernameCliente
            idea.save()
            return redirect('idea')
    else:
        form = IdeaForm()

    # Recupera todas las ideas de la base de datos
    ideas = Idea.objects.all().order_by('-fecha_creacion')
    
    # Agregar información del usuario a cada idea
    for idea in ideas:
        try:
            idea.usuario = UserClientes.objects.get(usernameCliente=idea.autor)
        except UserClientes.DoesNotExist:
            idea.usuario = None
    
    return render(request, 'core/idea.html', {
        'form': form,
        'ideas': ideas,
        'usuario': usuario,
    })

def empresa_ideas_view(request):
    """
    Vista para que las empresas gestionen las ideas.
    """
    ideas = Idea.objects.all().order_by('-fecha_creacion')
    
    if request.method == 'POST':
        idea_id = request.POST.get('idea_id')
        accion = request.POST.get('accion')
        
        if idea_id and accion:
            idea = Idea.objects.get(pk=idea_id)
            if accion == 'aceptar':
                idea.estado = 'en_proceso'
                idea.empresa_asignada = request.user.userempresa
                idea.save()
            elif accion == 'completar':
                idea.estado = 'completada'
                idea.save()
    
    return render(request, 'Empresas/ideas_empresa.html', {
        'ideas': ideas
    })
    
def perfilUsuario_view(request):
    username = request.session.get('usernameCliente')
    if not username:
        return redirect('login')
    
    try:
        usuario = UserClientes.objects.get(usernameCliente=username)
        context = {
            'usuario': usuario,
        }
        return render(request, 'core/perfilUsuario.html', context)
    except UserClientes.DoesNotExist:
        return redirect('login')

# Vistas para Comentarios
from .models import Comentario
from .forms import ComentarioForm, PerfilUsuarioForm
from django.contrib import messages
from django.urls import reverse

def comentarios_view(request):
    # Obtener el usuario de la sesión
    usernameCliente = request.session.get('usernameCliente')
    usuario = None
    if usernameCliente:
        try:
            usuario = UserClientes.objects.get(usernameCliente=usernameCliente)
        except UserClientes.DoesNotExist:
            pass
    
    # Obtener todos los comentarios ordenados por fecha
    comentarios = Comentario.objects.all().order_by('-fecha_creacion')
    
    context = {
        'comentarios': comentarios,
        'usuario': usuario,
    }
    return render(request, 'core/comentarios.html', context)

def crear_comentario_view(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            # Asignar el usuario actual al comentario
            # Aqu� asumimos que tienes el usuario en la sesi�n o autenticaci�n
            # Deber�s ajustar esto seg�n tu l�gica de autenticaci�n
            try:
                # Intenta obtener el usuario de la sesi�n
                username = request.session.get('usernameCliente')
                if username:
                    usuario = UserClientes.objects.get(usernameCliente=username)
                    comentario.usuario = usuario
                    comentario.save()
                    messages.success(request, 'Comentario publicado exitosamente')
                    return redirect('comentarios')
                else:
                    messages.error(request, 'Debes iniciar sesi�n para comentar')
                    return redirect('login')
            except UserClientes.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
                return redirect('login')
    else:
        form = ComentarioForm()
    
    return render(request, 'core/crear_comentario.html', {'form': form})

def eliminar_comentario_view(request, comentario_id):
    try:
        comentario = Comentario.objects.get(id=comentario_id)
        # Verificar que el usuario sea el due�o del comentario
        username = request.session.get('usernameCliente')
        if username:
            usuario = UserClientes.objects.get(usernameCliente=username)
            if comentario.usuario == usuario:
                comentario.delete()
                messages.success(request, 'Comentario eliminado exitosamente')
            else:
                messages.error(request, 'No tienes permiso para eliminar este comentario')
        else:
            messages.error(request, 'Debes iniciar sesi�n')
    except Comentario.DoesNotExist:
        messages.error(request, 'Comentario no encontrado')
    except UserClientes.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
    
    return redirect('comentarios')

# Vistas para Perfil de Usuario
def editar_perfil_view(request):
    username = request.session.get('usernameCliente')
    if not username:
        messages.error(request, 'Debes iniciar sesi�n para editar tu perfil')
        return redirect('login')
    
    try:
        usuario = UserClientes.objects.get(usernameCliente=username)
        
        if request.method == 'POST':
            form = PerfilUsuarioForm(request.POST, request.FILES, instance=usuario)
            if form.is_valid():
                # Verificar si se est�n cambiando las contrase�as
                password_actual = form.cleaned_data.get('passwordCliente_actual')
                password_nueva = form.cleaned_data.get('passwordCliente_nueva')
                
                if password_actual and password_nueva:
                    # Verificar que la contrase�a actual sea correcta
                    if usuario.passwordCliente == password_actual:
                        usuario.passwordCliente = password_nueva
                    else:
                        messages.error(request, 'La contrase�a actual es incorrecta')
                        return render(request, 'core/editar_perfil.html', {'form': form})
                
                # Guardar el formulario
                form.save()
                
                # Actualizar el username en la sesi�n si cambi�
                request.session['usernameCliente'] = usuario.usernameCliente
                request.session.modified = True
                
                messages.success(request, 'Perfil actualizado exitosamente')
                return redirect('perfilUsuario')
        else:
            form = PerfilUsuarioForm(instance=usuario)
        
        context = {
            'form': form,
            'usuario': usuario,
        }
        return render(request, 'core/editar_perfil.html', context)
    except UserClientes.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('login')

# Vistas para gestión de comentarios por Empresa
def empresa_comentarios_view(request):
    """Vista para que las empresas vean y gestionen comentarios"""
    # Verificar que sea una empresa autenticada
    empresa_username = request.session.get('usernameEmpresa')
    if not empresa_username:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    # Obtener todos los comentarios ordenados: pendientes primero, luego por fecha
    comentarios = Comentario.objects.all().order_by('estado', '-fecha_creacion')
    
    context = {
        'comentarios': comentarios,
    }
    return render(request, 'Empresas/gestion_comentarios.html', context)

def aprobar_comentario_view(request, comentario_id):
    """Vista para aprobar un comentario"""
    # Verificar que sea una empresa autenticada
    empresa_username = request.session.get('usernameEmpresa')
    if not empresa_username:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    try:
        comentario = Comentario.objects.get(id=comentario_id)
        comentario.estado = 'aprobado'
        comentario.fecha_aprobacion = timezone.now()
        comentario.save()
        messages.success(request, 'Comentario aprobado exitosamente')
    except Comentario.DoesNotExist:
        messages.error(request, 'Comentario no encontrado')
    
    return redirect('empresa_comentarios')

def rechazar_comentario_view(request, comentario_id):
    """Vista para rechazar un comentario"""
    # Verificar que sea una empresa autenticada
    empresa_username = request.session.get('usernameEmpresa')
    if not empresa_username:
        messages.error(request, 'Debes iniciar sesión como empresa')
        return redirect('loginEmpresa')
    
    try:
        comentario = Comentario.objects.get(id=comentario_id)
        comentario.estado = 'rechazado'
        comentario.fecha_aprobacion = None
        comentario.save()
        messages.success(request, 'Comentario rechazado')
    except Comentario.DoesNotExist:
        messages.error(request, 'Comentario no encontrado')
    
    return redirect('empresa_comentarios')

@require_http_methods(["POST"])
def procesar_pago(request):
    """Vista para procesar el pago con comprobante"""
    # Verificar que el usuario esté autenticado
    usernameCliente = request.session.get('usernameCliente')
    if not usernameCliente:
        return JsonResponse({'success': False, 'error': 'Usuario no autenticado'}, status=401)
    
    try:
        # Obtener el cliente
        cliente = UserClientes.objects.get(usernameCliente=usernameCliente)
        
        # Obtener datos del formulario
        metodo_pago = request.POST.get('metodo_pago')
        monto_total = request.POST.get('monto_total')
        productos = request.POST.get('productos')
        comprobante = request.FILES.get('comprobante')
        
        # Validar datos
        if not all([metodo_pago, monto_total, productos, comprobante]):
            return JsonResponse({'success': False, 'error': 'Faltan datos requeridos'}, status=400)
        
        # Crear el registro de pago
        pago = Pago.objects.create(
            cliente=cliente,
            metodo_pago=metodo_pago,
            monto_total=float(monto_total),
            comprobante=comprobante,
            productos=productos,
            estado='pendiente'
        )
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Pago registrado exitosamente',
            'pago_id': pago.id
        })
        
    except UserClientes.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cliente no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def crear_pedido_view(request, pago_id):
    """Vista para crear un pedido después de confirmar el pago"""
    # Verificar sesión de cliente
    if 'usernameCliente' not in request.session:
        return redirect('login')
    
    try:
        # Obtener cliente y pago
        cliente = UserClientes.objects.get(usernameCliente=request.session['usernameCliente'])
        pago = Pago.objects.get(id=pago_id, cliente=cliente)
        
        # Verificar que el pago esté confirmado
        if pago.estado != 'confirmado':
            return redirect('carrito')
        
        # Verificar que no exista ya un pedido para este pago
        if hasattr(pago, 'pedido'):
            return redirect('mis_pedidos')
        
        if request.method == 'POST':
            from datetime import timedelta
            from django.utils import timezone
            
            # Parsear productos antes de crear el pedido
            try:
                productos_lista = json.loads(pago.productos)
            except:
                productos_lista = []
            
            # Verificar y descontar inventario
            modelos_map = {
                'mesa': Mesas,
                'silla': Sillas,
                'armario': Armarios,
                'cajonera': Cajoneras,
                'escritorio': Escritorios,
                'utensilio': Utensilios,
            }
            
            # Verificar que haya suficiente inventario antes de descontar
            for item in productos_lista:
                tipo = item.get('tipo')
                producto_id = item.get('id')
                cantidad_pedida = item.get('cantidad', 0)
                
                modelo = modelos_map.get(tipo)
                if modelo:
                    try:
                        producto = modelo.objects.get(id=producto_id)
                        if producto.cantidad_disponible < cantidad_pedida:
                            return render(request, 'core/crear_pedido.html', {
                                'error': f'No hay suficiente inventario de {item.get("nombre")}. Disponible: {producto.cantidad_disponible}',
                                'pago': pago,
                                'productos': productos_lista,
                                'cliente': cliente
                            })
                    except modelo.DoesNotExist:
                        pass
            
            # Crear el pedido
            pedido = Pedido.objects.create(
                pago=pago,
                cliente=cliente,
                nombre_completo=request.POST.get('nombre_completo'),
                telefono=request.POST.get('telefono'),
                direccion=request.POST.get('direccion'),
                ciudad=request.POST.get('ciudad'),
                departamento=request.POST.get('departamento'),
                codigo_postal=request.POST.get('codigo_postal', ''),
                notas_adicionales=request.POST.get('notas_adicionales', ''),
                productos=pago.productos,
                monto_total=pago.monto_total,
                estado='procesando',
                fecha_entrega_estimada=timezone.now().date() + timedelta(days=7)
            )
            
            # Descontar del inventario
            for item in productos_lista:
                tipo = item.get('tipo')
                producto_id = item.get('id')
                cantidad_pedida = item.get('cantidad', 0)
                
                modelo = modelos_map.get(tipo)
                if modelo and cantidad_pedida > 0:
                    try:
                        producto = modelo.objects.get(id=producto_id)
                        producto.cantidad_disponible = max(0, producto.cantidad_disponible - cantidad_pedida)
                        producto.save()
                    except modelo.DoesNotExist:
                        pass
            
            return redirect('mis_pedidos')
        
        # Parsear productos del pago
        try:
            productos = json.loads(pago.productos)
        except:
            productos = []
        
        context = {
            'pago': pago,
            'productos': productos,
            'cliente': cliente
        }
        
        return render(request, 'core/crear_pedido.html', context)
        
    except (UserClientes.DoesNotExist, Pago.DoesNotExist):
        return redirect('carrito')

def mis_pedidos_view(request):
    """Vista para ver los pedidos del cliente"""
    # Verificar sesión de cliente
    if 'usernameCliente' not in request.session:
        return redirect('login')
    
    try:
        cliente = UserClientes.objects.get(usernameCliente=request.session['usernameCliente'])
        pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha_creacion')
        
        # Parsear productos para cada pedido
        for pedido in pedidos:
            try:
                pedido.productos_parseados = json.loads(pedido.productos)
            except:
                pedido.productos_parseados = []
        
        context = {
            'pedidos': pedidos,
            'cliente': cliente,
            'usuario': cliente  # Añadir para compatibilidad con el template
        }
        
        return render(request, 'core/mis_pedidos.html', context)
        
    except UserClientes.DoesNotExist:
        return redirect('login')

def detalle_pedido_view(request, pedido_id):
    """Vista para ver el detalle de un pedido específico"""
    # Verificar sesión de cliente
    if 'usernameCliente' not in request.session:
        return redirect('login')
    
    try:
        cliente = UserClientes.objects.get(usernameCliente=request.session['usernameCliente'])
        pedido = Pedido.objects.get(id=pedido_id, cliente=cliente)
        
        # Parsear productos
        try:
            pedido.productos_parseados = json.loads(pedido.productos)
        except:
            pedido.productos_parseados = []
        
        context = {
            'pedido': pedido,
            'cliente': cliente
        }
        
        return render(request, 'core/detalle_pedido.html', context)
        
    except (UserClientes.DoesNotExist, Pedido.DoesNotExist):
        return redirect('mis_pedidos')

def completar_datos_envio_view(request, pedido_id):
    """Vista para completar los datos de envío de un pedido"""
    if 'usernameCliente' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            cliente = UserClientes.objects.get(usernameCliente=request.session['usernameCliente'])
            pedido = Pedido.objects.get(id=pedido_id, cliente=cliente)
            
            # Actualizar datos de envío
            pedido.nombre_completo = request.POST.get('nombre_completo')
            pedido.telefono = request.POST.get('telefono')
            pedido.direccion = request.POST.get('direccion')
            pedido.ciudad = request.POST.get('ciudad')
            pedido.departamento = request.POST.get('departamento')
            pedido.codigo_postal = request.POST.get('codigo_postal', '')
            pedido.notas_adicionales = request.POST.get('notas_adicionales', '')
            
            pedido.save()
            
            return redirect('mis_pedidos')
            
        except (UserClientes.DoesNotExist, Pedido.DoesNotExist):
            return redirect('mis_pedidos')
    
    return redirect('mis_pedidos')

def get_cantidad_disponible_view(request):
    """Vista API para obtener la cantidad disponible de un producto"""
    tipo = request.GET.get('tipo')
    producto_id = request.GET.get('id')
    
    if not tipo or not producto_id:
        return JsonResponse({'error': 'Parámetros incompletos'}, status=400)
    
    try:
        modelos = {
            'mesa': Mesas,
            'silla': Sillas,
            'armario': Armarios,
            'cajonera': Cajoneras,
            'escritorio': Escritorios,
            'utensilio': Utensilios,
        }
        
        modelo = modelos.get(tipo)
        if not modelo:
            return JsonResponse({'error': 'Tipo de producto no válido'}, status=400)
        
        producto = modelo.objects.get(id=producto_id)
        
        # Obtener el nombre del producto según el tipo
        campo_nombre_map = {
            'mesa': 'nombre1',
            'silla': 'nombre2',
            'armario': 'nombre3',
            'cajonera': 'nombre4',
            'escritorio': 'nombre5',
            'utensilio': 'nombre6',
        }
        
        campo_nombre = campo_nombre_map.get(tipo)
        nombre_producto = getattr(producto, campo_nombre, 'Producto')
        
        return JsonResponse({
            'cantidad_disponible': producto.cantidad_disponible,
            'nombre': nombre_producto
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
