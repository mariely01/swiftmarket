from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Producto, Comentario
from .forms import ProductoForm
from .models import Compra, ProductoComprado



def inicio(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    else:
        productos = Producto.objects.all()
    comentarios = Comentario.objects.all().order_by('-fecha')  
    return render(request, 'tienda/inicio.html', {'productos': productos, 'comentarios': comentarios})


def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'tienda/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def registro(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')  
        correo = request.POST.get('email')  
        clave = request.POST.get('password')

        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
        elif User.objects.filter(email=correo).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
        else:
            user = User.objects.create_user(username=usuario, email=correo, password=clave)
            login(request, user)
            return redirect('inicio')

    return render(request, 'tienda/registro.html')


@staff_member_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoForm()
    return render(request, 'tienda/agregar_producto.html', {'form': form})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if producto_id in carrito:
        carrito[producto_id] += 1
    else:
        carrito[producto_id] = 1

    
    request.session['carrito'] = carrito
    return redirect('carrito')

def carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return render(request, 'tienda/carrito.html', {
        'productos': productos,
        'total': total
    })


@login_required
def comentar(request):
    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        if comentario_texto:
            Comentario.objects.create(usuario=request.user, texto=comentario_texto)
            messages.success(request, '¡Comentario enviado!')
        else:
            messages.error(request, 'Por favor, ingresa un comentario.')

    comentarios = Comentario.objects.all().order_by('-fecha')
    return render(request, 'tienda/inicio.html', {'comentarios': comentarios})


@login_required
def checkout(request):
   
    carrito = request.session.get('carrito', {})

    if not carrito:
        return redirect('inicio')

    compra = Compra.objects.create(usuario=request.user)
    total = 0  

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, pk=int(producto_id))
        subtotal = producto.precio * cantidad  
        total += subtotal  

        
        ProductoComprado.objects.create(
            compra=compra,
            producto=producto,
            cantidad=cantidad
        )

    
    compra.total = total
    compra.save()

    
    request.session['carrito'] = {}

    
    return render(request, 'tienda/checkout_exito.html', {'compra': compra, 'total': total})

@login_required
def compra_confirmada(request, compra_id):
    compra = Compra.objects.get(id=compra_id)
    productos_comprados = ProductoComprado.objects.filter(compra=compra)

    context = {
        'compra': compra,
        'productos_comprados': productos_comprados,
    }
    
    return render(request, 'compra_confirmada.html', context)

@login_required
def procesar_compra(request):
    if request.method == 'POST':
        
        compra = Compra.objects.create(usuario=request.user)
        
        for producto in productos_seleccionados:
            ProductoComprado.objects.create(compra=compra, producto=producto, cantidad=cantidad)

        return redirect('compra_confirmada', compra_id=compra.id)

@login_required
def historial_compras(request):
    compras = Compra.objects.filter(usuario=request.user) 

    return render(request, 'tienda/historial_compras.html', {'compras': compras})

@login_required
def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query) 
    return render(request, 'tienda/inicio.html', {'productos': productos, 'query': query})