# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from app.views import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'frente.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^redi$', 'app.views.home', name='home'),
    url(r'^frente/$', 'app.views.frente', name='frente'),
    url(r'^accounts/login/$', 'app.views.user_login', name="url_login"),
    url(r'^hqlogin/$', 'app.views.user_login', name="url_login"),
    url(r'^accounts/logout/$', 'app.views.user_logout', name="url_logout"),
    url(r'^frente/usuarionuevo/$', 'app.views.user_register', name="url_registro"),
    url(r'^distribucion/cliente/$', 'app.views.register_cliente', name="url_registrocliente"),
    url(r'^empresa/suscripcion/$', 'app.views.register_empresa', name="url_registroempresa"),
    url(r'^register/ruta/$', 'app.views.register_ruta', name="url_registroruta"),
    url(r'^register/repartidor/$', 'app.views.register_repartidor', name="url_registrorepartidor"),
    # url(r'^frente/suscripcion/$', 'app.views.register_frente', name="url_registrofrente"),
    # Empiezan Cupones
    url(r'^frente/cupones/$', 'app.views.ver_cupones', name="url_vercupones"),
    url(r'^frente/cupones/nuevo$', 'app.views.register_cupon', name="url_registrocupon"),
    url(r'^frente/cupones/lista/$', 'app.views.cupon_lista', name='cupones_lista'),
    url(r'^frente/cupones/editar/(?P<pk>\d+)$', 'app.views.cupon_edit', name='cupones_edit'),
    #Terminan cupones
    #Empieza usuarios
    url(r'^frente/usuarios/$', 'app.views.frente_usuarios', name="url_frenteusuarios"),
    url(r'^frente/usuarios/edit/(?P<id>[0-9]+)$', 'app.views.edit_frenteusuarios', name="url_frenteusuarios"),
    url(r'^frente/usuarios/delete/(?P<pk>\d+)$', 'app.views.frenteusuarios_delete', name='frenteusuarios_delete'),
    url(r'^frente/usuarios/password/(?P<bandera>\d+)$', 'app.views.contrasena_user', name='contrasena'),
    url(r'^distribucion/usuarios/password/(?P<bandera>\d+)$', 'app.views.contrasena_user', name='contrasena_masxmas'),
    # url(r'^frente/clientes/$', 'app.views.frente_clientes', name="url_frenteuclientes"),
    url(r'^frente/clientes/$', 'app.views.clientefrente_list', name='clientefrente_list'),
    url(r'^$', 'app.views.clientefrente_create', name='clientefrente_create_new'),
    url(r'^delegacion_ajax/$', delegacion_ajaxview.as_view(), name='delegacion_ajax'),
    url(r'^frente/clientes/editar/(?P<pk>\d+)$', 'app.views.clientefrente_update', name='clientefrente_edit'),
    url(r'^frente/clientes/ver/(?P<pk>\d+)$', 'app.views.clientefrente_view', name='clientefrente_view'),
    url(r'^frente/clientes/eliminar/(?P<pk>\d+)$', 'app.views.clientefrente_delete', name='clientefrente_delete'),
    url(r'^frente/clientes/final$', 'app.views.frente_clientesfinal', name='clientefrentefinal_list'),
    url(r'^promocion/(?P<cupon>\w+)/$', 'app.views.campania_forid', name='campania_forid'),
    #Membresias
    # url(r'^frente/membreisas/$', 'app.views.membreisas_list', name='clientefrente_list'),
    # url(r'^frente/membreisas/$', 'app.views.membreisas_create', name='membreisascreate_new'),
    # url(r'^frente/membreisas/editas/(?P<pk>\d+)$', 'app.views.membreisas_update', name='membreisas_edit'),
    # url(r'^frente/membreisas/ver/(?P<pk>\d+)$', 'app.views.membreisas_view', name='membreisas_view'),
    # url(r'^frente/membreisas/eliminar/(?P<pk>\d+)$', 'app.views.membreisas_delete', name='membreisas_delete'),
    #Termina Menresias
    #Campanias
    url(r'^frente/campania/$', 'app.views.campania_list', name='campania_list'),
    url(r'^frente/campania/nueva/$', 'app.views.campania_create', name='campania_create_new'),

    url(r'^frente/campania/activa/$', 'app.views.campanialist_frente', name='campanialist_frente'),
    url(r'^frente/campania/inactiva/$', 'app.views.campanialistFalse_frente', name='campanialistFalse_frente'),

    url(r'^frente/campania/lista$', 'app.views.campania_listaedit', name='campania_listedit'),
    url(r'^frente/campania/editar/(?P<pk>\d+)$', 'app.views.campania_update', name='campania_edit'),
    url(r'^frente/campania/ver/(?P<pk>\d+)$', 'app.views.campania_view', name='campania_view'),
    url(r'^frente/campania/eliminar/(?P<pk>\d+)$', 'app.views.campania_delete', name='campania_delete'),
    #Termina Campanias
    #Campanias
    url(r'^frente/aliados/$', 'app.views.aliados_list', name='aliados_list'),
    url(r'^frente/aliados/nuevo/$', 'app.views.aliados_create', name='aliados_create_new'),
    url(r'^frente/aliados/lista$', 'app.views.aliados_listaedit', name='aliados_listedit'),
    url(r'^frente/aliados/editar/(?P<pk>\d+)$', 'app.views.aliados_update', name='aliados_edit'),
    url(r'^frente/aliados/ver/(?P<pk>\d+)$', 'app.views.aliados_view', name='aliados_view'),
    url(r'^frente/aliados/eliminar/(?P<pk>\d+)$', 'app.views.aliados_delete', name='aliados_delete'),
    #Termina Campanias
    # url(r'^frente/clientes/edit/(?P<id>[0-9]+)$', 'app.views.edit_frenteclientes', name="url_editfrenteclientes"),

    # QUEJAS
    url(r'^quejas/$', 'app.views.quejas', name='quejas'),
    url(r'^frente/quejas/(?P<queja>\d+)$', 'app.views.consulta_quejas', name='consulta_quejas'),
    url(r'^frente/quejas/(?P<queja>\d+)/ver/(?P<id>\d+)$', 'app.views.ver_quejas', name='ver_quejas'),
    url(r'^distribucion/quejas/(?P<queja>\d+)$', 'app.views.consulta_quejas', name='consulta_quejasmasxmas'),
    url(r'^distribucion/quejas_baja/(?P<queja>\d+)$', 'app.views.consulta_quejas_baja', name='consulta_quejasmasxmas_baja'),
    url(r'^distribucion/quejas/(?P<queja>\d+)/ver/(?P<id>\d+)$', 'app.views.ver_quejas', name='ver_quejasmasxmas'),
    url(r'^distribucion/quejas_solucion/(?P<id>\d+)$', 'app.views.quejas_solucion_masxmas', name='quejas_solucion_masxmas'),

    #MAS X MAS
    url(r'^distribucion/$', 'app.views.masxmas', name='masxmas'),
    url(r'^distribucion/inactivos$', 'app.views.masxmas_inactivos', name='masxmas_inactivos'),
    url(r'^distribucion/busqueda$', 'app.views.searchCliente', name='searchCliente'),
    url(r'^distribucion/newclient$', 'app.views.clientesnuevos', name='clientesnuevos'),
    url(r'^distribucion/edit/cliente/(?P<id>\d+)$', 'app.views.edit_clientesmasxmas', name='edit_clientesmasxmas'),
    url(r'^distribucion/show/cliente/(?P<id>\d+)$', 'app.views.ShowCliente', name='ShowCliente'),

    #Rutas
    url(r'^distribucion/rutas/$', 'app.views.rutas_list', name='rutas_list'),
    url(r'^distribucion/rutas/edit/(?P<id>\d+)$', 'app.views.rutas_edit', name='rutas_edit'),
    url(r'^distribucion/rutas/new$', 'app.views.rutas_new', name='rutas_new'),

    #Repartidores
    url(r'^distribucion/repartidores/$', 'app.views.reportidores_list', name='reportidores_list'),
    url(r'^distribucion/repartidor/edit/(?P<id>\d+)$', 'app.views.repartidor_edit', name='repartidor_edit'),
    url(r'^distribucion/repartidor/new$', 'app.views.repartidor_new', name='repartidor_new'),
    url(r'^distribucion/repartidores/rutas/(?P<id>\d+)$', 'app.views.repartidor_ver', name='repartidor_ver'),
    url(r'^distribucion/dotacion/$', 'app.views.changeDotacion', name='changeDotacion'),

    #Categoria
    url(r'^distribucion/categoria/$', 'app.views.categoria_list', name='categoria_list'),
    url(r'^distribucion/categoria/edit/(?P<id>\d+)$', 'app.views.categoria_edit', name='categoria_edit'),
    url(r'^distribucion/categoria/new$', 'app.views.categoria_new', name='categoria_new'),
    url(r'^distribucion/categoria/filter/(?P<id>\d+)$', 'app.views.categoria_filter', name='categoria_filter'),

    #SUBCategoria1
    url(r'^distribucion/subcategoria1/$', 'app.views.subcategoria1_list', name='subcategoria1_list'),
    url(r'^distribucion/subcategoria1/edit/(?P<id>\d+)$', 'app.views.subcategoria1_edit', name='subcategoria1_edit'),
    url(r'^distribucion/subcategoria1/filter/(?P<id>\d+)$', 'app.views.subcategoria1_filter', name='subcategoria1_filter'),
    url(r'^distribucion/subcategoria1/new$', 'app.views.subcategoria1_new', name='subcategoria1_new'),

    #SUBCategoria2
    url(r'^distribucion/subcategoria2/$', 'app.views.subcategoria2_list', name='subcategoria2_list'),
    url(r'^distribucion/subcategoria2/edit/(?P<id>\d+)$', 'app.views.subcategoria2_edit', name='subcategoria2_edit'),
    url(r'^distribucion/subcategoria2/filter/(?P<id>\d+)$', 'app.views.subcategoria2_filter', name='subcategoria2_filter'),
    url(r'^distribucion/subcategoria2/new$', 'app.views.subcategoria2_new', name='subcategoria2_new'),

    #SUBCategoria3
    url(r'^distribucion/subcategoria3/$', 'app.views.subcategoria3_list', name='subcategoria3_list'),
    url(r'^distribucion/subcategoria3/edit/(?P<id>\d+)$', 'app.views.subcategoria3_edit', name='subcategoria3_edit'),
    url(r'^distribucion/subcategoria3/filter/(?P<id>\d+)$', 'app.views.subcategoria3_filter', name='subcategoria3_filter'),
    url(r'^distribucion/subcategoria3/new$', 'app.views.subcategoria3_new', name='subcategoria3_new'),

    #CAMPAÑASMASXMAS
    url(r'^distribucion/campania/activa$', 'app.views.campanialist', name='campanialist'),
    url(r'^distribucion/campania/desactivada$', 'app.views.campanialistFalse', name='campanialistFalse'),
    url(r'^distribucion/campania/clientes/(?P<cupon>\w+)/$', 'app.views.clientescupones', name='clientescupones'),
    url(r'^distribucion/campania/desactivar_campana/(?P<cupon>\w+)/$', 'app.views.desactivar_campana', name='desactivar_campana'),

    #DISTRIBUCION O CONTROL
    url(r'^distribucion/$', 'app.views.distribucion', name='distribucion'),
    url(r'^distribucion/new/cliente$', 'app.views.createClienteContro', name='createClienteContro'),
    url(r'^distribucion/busqueda$', 'app.views.searchClienteControl', name='searchClienteControl'),
    url(r'^distribucion/usuarios/delete/(?P<pk>\d+)$', 'app.views.bajaControl', name='bajaControl'),
    # url(r'^distribucion/show/cliente/(?P<id>\d+)$', 'app.views.ShowClienteControl', name='ShowClienteControl'),
    url(r'^distribucion/quejas_clientes/(?P<pk>\d+)$', 'app.views.quejasControl', name='quejasControl'),

    #CSV
    url(r'^csv/$', 'app.views.some_view', name='csv'),
    url(r'^csvrepa/(?P<id>\d+)$', 'app.views.rutas_export', name='csvrepa'),
    url(r'^parse/$', 'app.views.clientesparse', name='clientesparse'),
    url(r'^parsedele/$', 'app.views.parsedele', name='parsedele'),
    url(r'^parsecol/$', 'app.views.parsecol', name='parsecol'),
    url(r'^parsempe/$', 'app.views.parsempe', name='parsempe'),
    url(r'^parserutas/$', 'app.views.parserutas', name='parserutas'),
    url(r'^pasrsesub3/$', 'app.views.pasrsesub3', name='pasrsesub3'),
    url(r'^parserepa/$', 'app.views.parserepa', name='parserepa'),

    url(r'^export_info/(?P<nr>\d+)$', 'app.views.export_info', name='export_info'),
    url(r'^tags/(?P<nr>\d+)$', 'app.views.tags', name='tags'),

    #Mails
    # url(r'^mails/$', 'app.views.mails_suscripcion', name='mail'),

    #PR
    url(r'^pr/$', 'app.views.pr', name='pr'),
    url(r'^pr/cupon/ver$', 'app.views.pr_cupones_ver', name='pr_cupones_ver'), 

)
