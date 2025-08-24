from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import LoginForm, LoginFormAdmin, AgregarForm
from .models import UserClientes, UserAdmin, Mesas, Sillas, Armarios, Cajoneras, Escritorios, Utensilios
from .logic import obtener_respuesta

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
    return render(request,"core/home.html")

def about(request):
    return render(request,"core/about.html")

def portafolio(request):
    return render(request,"core/portafolio.html")

def productos(request):
    return render(request,"core/productos.html")

def contact(request):
    return render(request,"core/contact.html")

def Login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usernameCliente = form.cleaned_data['usernameCliente']
            passwordCliente = form.cleaned_data['passwordCliente']
            email = form.cleaned_data['email']
            try:
                user = UserClientes.objects.get(usernameCliente=usernameCliente, passwordCliente=passwordCliente, email=email)
                return redirect('home2')
            except UserClientes.DoesNotExist:
                error_message = "Usuario o contraseña incorrectos"
                return render(request, 'core/login.html', {'error_message': error_message})
    else:
        form = LoginForm()
    return render(request,'core/login.html', {'form': form})

def LoginAdmin_view(request):
    if request.method == 'POST':
        form = LoginFormAdmin(request.POST)
        if form.is_valid():
            usernameAdmin = form.cleaned_data['usernameAdmin']
            passwordAdmin = form.cleaned_data['passwordAdmin']
            try:
                userAdmin = UserAdmin.objects.get(usernameAdmin=usernameAdmin, passwordAdmin=passwordAdmin)
                return redirect('dashboard')
            except UserAdmin.DoesNotExist:
                error_message = "Usuario o contraseña incorrectos"
                return render(request, 'core/loginAdmin.html', {'error_message': error_message})
    else:
        form = LoginFormAdmin()
    return render(request,'core/loginAdmin.html', {'form': form})

def Logout_view(request):
    logout(request)
    return redirect('home')

def Home2_view(request):
    return render(request,'core/home2.html')

def Home3_view(request):
    return render(request,'core/home3.html')

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
    return render(request,"core/idea.html")

def carrito(request):
    return render(request,"core/carrito.html")

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
