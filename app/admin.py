from django.contrib import admin
from app.models import *

# Register your models here.
class RutaAdmin(admin.ModelAdmin):
	list_display =['descripcion_Ruta', 'numero_Ruta','id']
admin.site.register(Ruta, RutaAdmin)

class RepartidorAdmin(admin.ModelAdmin):
	list_display = ['nombre', 'apellido_Paterno']
	search_fields = ['nombre','rutas']
admin.site.register(Repartidor, RepartidorAdmin)

class ClienteAdmin(admin.ModelAdmin):
	list_display = ['nombre',]
	list_filter = ['created']
	search_fields =['nombre','puesto','created','mail']
admin.site.register(Cliente, ClienteAdmin)

class EmpresaAdmin(admin.ModelAdmin):
	list_display = ['nombreEmpresa','id']
	list_filter = ['created']
	search_fields =['nombreEmpresa']
admin.site.register(Empresa, EmpresaAdmin)

class ClienteFrenteAdmin(admin.ModelAdmin):
	list_display = ['nombre','apellido_Paterno','delegacion','id']
	list_filter = ['created']
	search_fields =['nombre','apellido_Paterno','mail','calle','delegacion','ciudad','colonia','created','subcategoria1','subcategoria2','subcategoria3']
admin.site.register(ClienteFrente, ClienteFrenteAdmin)

class DelegacionFrenteAdmin(admin.ModelAdmin):
	list_display = ['descripcion_Delegacion', 'id']
	list_filter =['descripcion_Delegacion']
admin.site.register(Delegacion_frente,DelegacionFrenteAdmin)

class ColoniafrenteAdmin(admin.ModelAdmin):
	list_display = ['descripcion_Colonia', 'id']
	list_filter =['delegacion']
	search_fields = ['descripcion_Colonia']
admin.site.register(Colonia_frente,ColoniafrenteAdmin)

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ['descripcion_Categoria', 'id']
	list_filter =['descripcion_Categoria']
	search_fields = ['descripcion_Categoria','created']
admin.site.register(Categoria,CategoriaAdmin)

class Canal_distribucionAdmin(admin.ModelAdmin):
	list_display = ['descripcion_Distribucion', 'id']
	list_filter =['descripcion_Distribucion']
	search_fields = ['descripcion_Distribucion','created']
admin.site.register(Canal_distribucion,Canal_distribucionAdmin)

class Subcategoria1Admin(admin.ModelAdmin):
	list_display = ['descripcion_SubCategoria1', 'id']
	list_filter =['descripcion_SubCategoria1']
	search_fields = ['descripcion_SubCategoria1','created']
admin.site.register(Subcategoria1,Subcategoria1Admin)

class Subcategoria2Admin(admin.ModelAdmin):
	list_display = ['descripcion_SubCategoria2', 'id']
	list_filter =['descripcion_SubCategoria2']
	search_fields = ['descripcion_SubCategoria2','created']
admin.site.register(Subcategoria2,Subcategoria2Admin)

class Subcategoria3Admin(admin.ModelAdmin):
	list_display = ['descripcion_SubCategoria3', 'id']
	list_filter =['descripcion_SubCategoria3']
	search_fields = ['descripcion_SubCategoria3','created']
admin.site.register(Subcategoria3,Subcategoria3Admin)

class CuponAdmin(admin.ModelAdmin):
	list_display =['cupon','usuariogen', 'activo','campania']
	list_filter = ['cupon','usuariogen']
	search_fields = ['cupon','created','usuariogen','mail_cliente','campania']
admin.site.register(Cupon,CuponAdmin)

class MembresiaAdmin(admin.ModelAdmin):
	list_display =['descripcion','duracion']
	list_filter = ['descripcion','duracion']
	search_fields = ['descripcion','duracion']
admin.site.register(Membresia,MembresiaAdmin)

class CuponeraAdmin(admin.ModelAdmin):
	list_display =['fechainicio','fechafinal']
	list_filter = ['fechainicio','fechafinal','cliente','cupon']
	search_fields = ['fechainicio','fechafinal','cliente','cupon']
admin.site.register(Cuponera,CuponeraAdmin)

class CampaniaAdmin(admin.ModelAdmin):
	list_display =['descripcion']
	list_filter = ['descripcion']
	search_fields = ['descripcion']
admin.site.register(Campania,CampaniaAdmin)

class AliadosAdmin(admin.ModelAdmin):
	list_display =['descripcion']
	list_filter = ['descripcion']
	search_fields = ['descripcion','campania']
admin.site.register(Aliados,AliadosAdmin)

class QuejaAdmin(admin.ModelAdmin):
	list_display =['Nombre','Tipo_queja']
	list_filter = ['Nombre']
	search_fields = ['Nombre','Tipo_queja']
admin.site.register(Queja,QuejaAdmin)