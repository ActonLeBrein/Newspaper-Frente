# -*- coding: utf-8 -*-
from django.db import models
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from django.core.urlresolvers import reverse

# Create your models here.
class Delegacion(models.Model):
	descripcion_Delegacion = models.CharField(max_length=50)

	def __unicode__(self):
		return u'%s' % self.descripcion_Delegacion

class Colonia(models.Model):
	descripcion_Colonia = models.CharField(max_length=100)
	delegacion = models.ForeignKey(Delegacion)

	def __unicode__(self):
		return u'%s' % self.descripcion_Colonia

class Delegacion_frente(models.Model):
	descripcion_Delegacion = models.CharField(max_length=50)

	class Meta:
		ordering = ["descripcion_Delegacion"]

	def __unicode__(self):
		return u'%s' % self.descripcion_Delegacion

class Colonia_frente(models.Model):
	descripcion_Colonia = models.CharField(max_length=100)
	delegacion = models.ForeignKey(Delegacion_frente)

	def __unicode__(self):
		return u'%s' % self.descripcion_Colonia

class Ruta(models.Model):
	numero_Ruta = models.IntegerField()
	descripcion_Ruta = models.CharField(max_length=50)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.descripcion_Ruta

class Repartidor(models.Model):
	nombre = models.CharField(max_length=50)
	apellido_Paterno = models.CharField(max_length=50)
	apellido_Materno = models.CharField(max_length=50)
	rutas = models.ForeignKey(Ruta)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.nombre
    

class Categoria(models.Model):
	descripcion_Categoria = models.CharField(max_length= 100)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.descripcion_Categoria

class Canal_distribucion(models.Model):
	descripcion_Distribucion = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.descripcion_Distribucion

class Subcategoria1(models.Model):
	descripcion_SubCategoria1 = models.CharField(max_length = 100)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.descripcion_SubCategoria1

class Subcategoria2(models.Model):
	descripcion_SubCategoria2 = models.CharField(max_length = 100)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.descripcion_SubCategoria2

class Subcategoria3(models.Model):
	descripcion_SubCategoria3 = models.CharField(max_length = 100)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.descripcion_SubCategoria3    

class Aliados(models.Model):
    class Meta:
        verbose_name = ('Aliado')
        verbose_name_plural = ('Aliados')

    descripcion = models.CharField(max_length=100, null= True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
    	return u'%s' % self.descripcion

class Campania(models.Model):
    class Meta:
        verbose_name = ('Campania')
        verbose_name_plural = ('Campanias')

    descripcion = models.CharField(max_length= 50, null= False)
    activo = models.BooleanField(default=True)
    aliado = models.ForeignKey(Aliados, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.descripcion
		
class Cliente(models.Model):
	nombre = models.CharField(max_length=50)
	apellido_Materno = models.CharField(max_length=50)
	apellido_Paterno = models.CharField(max_length=50)
	puesto = models.CharField(max_length=50)
	telefono = models.IntegerField(max_length=10, unique=True, validators=[RegexValidator(regex='^\d{10}$', message='Debe de se de  10 digitos', code='Invalid number')])
	mail = models.EmailField(max_length=75)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.nombre

class Empresa(models.Model):
	nombreEmpresa = models.CharField(max_length=100, null=False)
	position = GeopositionField(null=True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s' % self.nombreEmpresa	
		
class Membresia(models.Model):
	descripcion = models.CharField(max_length= 100, null= False)
	duracion = models.IntegerField(max_length= 10, null= False)

	def __unicode__(self):
		return u'%s' % self.descripcion

class Cupon(models.Model):
	cupon = models.CharField(max_length=20, unique=True)
	cantidad = models.PositiveSmallIntegerField(max_length=50, null=True, blank=True)
	cuponusado = models.PositiveSmallIntegerField(max_length=50, null= True, blank=True, default=0)
	activo = models.BooleanField(default=True)
	mail_cliente = models.EmailField(max_length = 50,  null = True)
	fechafinal = models.DateTimeField(null=True)
	usuariogen = models.ForeignKey(User, null=True, limit_choices_to=Q( groups__name = 'PR'), blank=True)
	campania = models.ForeignKey(Campania, null= True)
	membresia = models.ForeignKey(Membresia, null= True)
	created = models.DateTimeField(auto_now_add=True)
	# usuario = models.ForeignKey(ClienteFrente, null=True)
	def __unicode__(self):
		return u'%s' % self.cupon

	def get_absolute_url(self):
		return reverse('cupon_edit', kwargs={'pk': self.pk})	

class Cuponera(models.Model):
	fechainicio = models.DateField(auto_now_add=True)
	fechafinal = models.DateField()
	cliente = models.ForeignKey(Cliente)
	cupon = models.ForeignKey(Cupon)

class ClienteFrente(models.Model):
	CHOICES=[('casa','Casa'),
         ('caseta de vigilancia','Caseta de Vigilancia'),
         	('oficina', 'Oficina')]
	OPCIONES=[('ETIQUETA Y EMBOLSADO','ETIQUETA Y EMBOLSADO'),
			('ETIQUETA','ETIQUETA'),
			('NO APLICA', 'NO APLICA ')]
	DAYS=[('Lunes','Lunes'),
		  ('Martes','Martes'),
		  ('Miercoles','Miercoles'),
		  ('Jueves','Jueves'),
		  ('Viernes','Viernes'),
		  ('Sabado','Sabado'),
		  ('Domingo','Domingo')]
	nombre = models.CharField(max_length=100)
	apellido_Paterno = models.CharField(max_length=100, null=False)
	apellido_Materno = models.CharField(max_length=100, null=True, blank=True)
	cumpleanos = models.DateField(auto_now=False)
	telefono = models.IntegerField(max_length=15, null=True, blank=True)
	phone = models.CharField(max_length=10, null=False)
	mail = models.EmailField(max_length=75, null=False)
	calle = models.CharField(max_length=100)
	cp = models.IntegerField(max_length= 10)
	numero_Exterior = models.IntegerField(max_length=10000)
	numero_Interior = models.CharField(max_length=50, null=True,blank=True)
	Colonia = models.ForeignKey(Colonia_frente)
	delegacion = models.ForeignKey(Delegacion_frente)
	entregas = models.CharField(max_length= 50, null=False, choices = CHOICES)
	cupon = models.CharField(max_length= 4, null=True)	
	empresa = models.ForeignKey(Empresa, null=True, blank=True)
	puesto = models.CharField(max_length=100, null=True, blank=True)
	referencia = models.CharField(max_length=150, null=True, blank=True)
	fvencimiento = models.DateField(auto_now=False, null=True)
	activo = models.BooleanField(default=True)
	rutas = models.ForeignKey(Ruta, null=True)
	categoria = models.ForeignKey(Categoria, null=True)
	subcategoria1 = models.ForeignKey(Subcategoria1, null=True)
	subcategoria2 = models.ForeignKey(Subcategoria2, null=True)
	subcategoria3 = models.ForeignKey(Subcategoria3, null=True)
	distribucion = models.ForeignKey(Canal_distribucion,null=True)
	dotacion = models.PositiveSmallIntegerField(max_length=50, null= True, blank=True, default=1)
	total = models.IntegerField(max_length=50, null= True, blank=True, default=1)
	adicional = models.IntegerField(max_length=50, null= True, blank=True, default=1)
	created = models.DateTimeField(auto_now_add=True)
	orden_entrega = models.CharField(max_length=100, null=True, blank=True)
	ordenentrega = models.PositiveSmallIntegerField(max_length=100, null=True, blank=True)
	embolsado = models.CharField(max_length= 50, null=False, choices = OPCIONES)
	day = models.CharField(max_length=10, choices = DAYS)

	def __unicode__(self):
		return u'%s,%s,%s' % (self.nombre, self.apellido_Paterno, self.apellido_Materno)

	def get_absolute_url(self):
		return reverse('server_edit', kwargs={'pk': self.pk})

# , validators=[RegexValidator(regex='^\d{10}$', message='Debe de ser 10 digitos', code='Invalid number')]


class Queja(models.Model):
    class Meta:
        verbose_name = ('Queja')
        verbose_name_plural = ('Quejas')

    MQueja=[('Ejemplar no recibido','Ejemplar no recibido'),
    		('Obsequio no recibido','Obsequio no recibido'),
			('Producto no recibido', 'Producto no recibido '),
			('Factura datos incorrectos', 'Factura datos incorrectos'),
			('Factura No recibida', 'Factura No recibida'),
			('Diferencia de Precio', 'Diferencia de Precio'),
			('Ejemplar Defectuoso', 'Ejemplar Defectuoso'),
			('Producto Defectuoso', 'Producto Defectuoso'),
			('Obsequio Defectuoso', 'Obsequio Defectuoso'),
			('Cancelación', 'Cancelación'),
			('Mal Servicio', 'Mal Servicio'),
			('Se queja del contenido', 'Se queja del contenido'),
			('Reposicion no recibida', 'Reposicion no recibida'),
			('Reincidente', 'Reincidente')]

    Nombre = models.CharField(max_length=50, null=False,blank=False)
    Correo = models.EmailField(max_length=80, null=False,blank=False)
    Telefono = models.CharField(max_length=10, null=True,blank=True)
    Queja = models.TextField(max_length=500, null=True,blank=True)
    Tipo_queja = models.CharField(max_length=50, null=True,blank=True, choices = MQueja)
    activada = models.BooleanField(default=True)
    solucion = models.TextField(max_length=500, null=False,blank=False)
    id_cliente = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' %self.Nombre
