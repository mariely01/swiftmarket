from django.db import models
from django.contrib.auth.models import User  

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comentario de {self.usuario.username} - {self.fecha}'

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    productos = models.ManyToManyField(Producto, through='ProductoComprado')  
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.usuario.username} en {self.fecha}"
        
class ProductoComprado(models.Model):
    compra = models.ForeignKey(Compra, related_name='producto_comprado', on_delete=models.CASCADE)  
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
