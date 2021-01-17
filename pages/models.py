from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titulo")
    content = RichTextField(verbose_name="Contenido")
    slug = models.CharField(unique=True, max_length=150, verbose_name="URL")
    order = models.IntegerField(default=0,verbose_name="Orden")
    visible = models.BooleanField(verbose_name="¿Visible?") 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Pagina"
        verbose_name_plural = "Paginas"
    
    def __str__(self):
        return self.title

class Juego (models.Model):
    nombre = models.CharField(max_length=50)
    cod_juego = models.CharField(max_length=15, verbose_name='Codigo Juego')
    tienda = models.CharField(max_length=25)
    precio = models.IntegerField()
    enlace = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el ')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Editado el ')

    def __str__(self):
        return f"{self.cod_juego} - {self.nombre} - {self.id}"

class Detalle_Juego (models.Model):
    cod_juego = models.CharField(max_length=15)
    descripcion = RichTextField(verbose_name="Descripcion")
    link_imagen = models.TextField(default='null')
    titulo_juego = models.CharField(max_length=50,default='null')

    def __str__(self):
        return f"{self.cod_juego}"

class Game (models.Model):
    nombre = models.CharField(max_length=50)
    cod_juego = models.CharField(max_length=15, verbose_name='Codigo Juego')
    tienda1 = models.CharField(max_length=25, verbose_name='Zmart')
    tienda2 = models.CharField(max_length=25, verbose_name='MicroPlay')
    tienda3 = models.CharField(max_length=25, verbose_name='Weplay')
    precio1 = models.IntegerField(verbose_name='Precio Zmart')
    precio2 = models.IntegerField(verbose_name='Precio Microplay')
    precio3 = models.IntegerField(verbose_name='Precio Weplay')
    preciomasbajo = models.IntegerField(verbose_name='Precio mas bajo')
    enlace1 = models.CharField(max_length=250, verbose_name='Link Zmart')
    enlace2 = models.CharField(max_length=250, verbose_name='Link MicroPlay')
    enlace3 = models.CharField(max_length=250, verbose_name='Link Weplay')
    desc = RichTextField(default='null', verbose_name="Descripcion")
    link_imagen = models.TextField(default='null')
    created_at = models.DateTimeField(verbose_name='Creado el ')
    updated_at = models.DateTimeField(verbose_name='Editado el ')

    def __str__(self):
        return f"{self.cod_juego} - {self.nombre} - {self.id}"

class Game_Detail (models.Model):
    cod_juego = models.CharField(max_length=15)
    descripcion = RichTextField(verbose_name="Descripcion")
    link_imagen = models.TextField(default='null')
    titulo_juego = models.CharField(max_length=50,default='null')

    def __str__(self):
        return f"{self.titulo_juego} - {self.cod_juego}"