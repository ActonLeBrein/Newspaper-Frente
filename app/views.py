# -*- coding: utf-8 -*-
import datetime
import simplejson
from django.utils.encoding import *
from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.context_processors import csrf
from django.core import serializers
from django.contrib.auth.forms import PasswordChangeForm
from datetime import tzinfo, timedelta, datetime, date
from django.utils import timezone
from app.forms import *
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import mailchimp
from mailchimp import utils
import random
import csv
import reportlab
from io import BytesIO
from reportlab.pdfgen import canvas
######################################
import SimpleHTTPServer
import SocketServer
import StringIO
import xlsxwriter
import os
from django.db.models import Count, Sum
from math import *

@login_required(login_url='/accounts/login/')
def home(request):
    if request.user:
        if request.user.groups.filter(name='Frente').count() >= 1:
            return redirect('clientefrente_list')
        elif request.user.groups.filter(name='MasxMas').count() >= 1:
            return redirect('masxmas')
        elif request.user.groups.filter(name='PR').count() >= 1:
            return redirect('pr')
        elif request.user.groups.filter(name='Distribucion').count() >= 1:
            return redirect('distribucion')

def user_login(request):
    form = LoginForm()
    if request.method == "POST":
    	form = LoginForm(request.POST)
    	if form.is_valid():
    		usuario = form.cleaned_data['username']
    		password = form.cleaned_data['password']
    		user = authenticate(username=usuario, password=password)
    		if user is not None:
    			if user.is_active:
    				login(request, user)
    				return HttpResponseRedirect('/redi')
    			else:
    				ctx = {"form":form, "mensaje": "Usuario Inactivo"}
    				return render_to_response("login.html",ctx, context_instance=RequestContext(request))
    		else:
    			ctx = {"form":form, "mensaje": "Datos incorrecto"}
    			return render_to_response("login.html",ctx, context_instance=RequestContext(request))	
 
    ctx = {"form":form, "mensaje":""}
    return render_to_response("login.html",ctx, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')  
def contrasena_user(request, bandera ):
    template_name = ""
    if bandera == "1":
        template_name='usuarios/contrasena.html'
    elif bandera == "2":
        template_name='usuarios/contrasenamasxmas.html'
    elif bandera == "3":
        template_name='usuarios/contrasenapr.html'
    form = PasswordChangeForm(data=request.POST or None, user = request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            ctx = {"form":form, "mensaje":"Nueva Contra Establecida"}
            return render_to_response(template_name,ctx, context_instance=RequestContext(request))
        else:
            ctx = {"form":form, "mensaje":"La Contrasenas no coinciden"}
            return render_to_response(template_name,ctx, context_instance=RequestContext(request))
    else:
        ctx = {"form":form, "mensaje":"", "bandera":bandera}
        return render_to_response(template_name,ctx, context_instance=RequestContext(request))

# User Logout View
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

# User Register View
@login_required(login_url='/accounts/login/')
def user_register(request):
    if request.user:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.groups.add(Group.objects.get(name='PR'))
                return HttpResponseRedirect('/frente/usuarios/')
        else:
            form = UserRegisterForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render_to_response('frente/registropr.html', context)
    else:
        form = UserRegisterForm()
    ctx = {"form":form, "mensaje":""}
    return render_to_response("frente/registropr.html",ctx, context_instance=RequestContext(request))

def register_cliente(request):
    if request.method == "POST":
        form_a = CreateCliente(request.POST, prefix="cli")
        form_b = CreateEmpresa(request.POST, prefix="emp")
        if form_a and form_b.is_valid():
            cliente = form_a.save()
            empresa = form_b.save(commit=False)
            empresa.cliente = cliente
            empresa.save()
            return HttpResponse('registro Realisado')
        else:
            form_a = CreateCliente(prefix="cli")
            form_b = CreateEmpresa(prefix="emp")
        context = {}
        context.update(csrf(request))
        context['form_a'] = form_a
        context['form_b'] = form_b
        #Pass the context to a template
        return render_to_response('registercliente.html', context)
    else:
        form_a = CreateCliente(prefix="cli")
        form_b = CreateEmpresa(prefix="emp")
        return render(request, 'registercliente.html', {'form_a': form_a,'form_b': form_b})

def register_empresa(request):
    form = CreateEmpresa()
    if request.method == "POST":
        form = CreateEmpresa(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/register/cliente/')
        else:
            return HttpResponse('algo salio mal')
            form = CreateEmpresa()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render_to_response('registerempresa.html', context)
    else:
        return render(request, 'registerempresa.html', {'form': form})

def register_ruta(request):
    form = CreateRuta()
    if request.method == "POST":
        form = CreateRuta(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Ruta Registrada')
        else:
            form = CreateRuta()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render_to_response('registerempresa.html', context)
    else:
        return render(request, 'registerempresa.html', {'form': form})

def register_repartidor(request):
    form = CreateRepartidor()
    if request.method == "POST":
        form = CreateRepartidor(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Repartidor Registrado')
        else:
            form = CreateRepartidor()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render_to_response('registerempresa.html', context)
    else:
        return render(request, 'registerempresa.html', {'form': form})

# Clientes de frente
@login_required(login_url='/accounts/login/')
def clientefrente_list(request, template_name='frente/clientes.html'):
    servers = ClienteFrente.objects.all().order_by('apellido_Paterno')
    startdate = datetime.today().date()
    paginator = Paginator(servers, 20)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    # for date in servers:
    #     print  date.fvencimiento
    # a = viewcliente.fvencimiento - relativedelta(months = 1)
    # if startdate >= a and startdate <= startdate:
    #     fecha = True
    # else:
    #     fecha = False
    data = {}
    data['cli'] = clientes
    # data['fecha'] = fecha
    return render_to_response(template_name, data)
    
def clientefrente_create(request, template_name='frente/frenteregistro.html'):
    startdate = datetime.today()
    form = CreateClienteFrente(request.POST or None)
    formem = EmpresaForm(request.POST or None, initial={'nombreEmpresa': ' '})
    if form.is_valid() and formem.is_valid():
        cuponvalid= form.cleaned_data['cupon']
        empresas = formem.cleaned_data['nombreEmpresa']
        try:
            cupon_valid = Cupon.objects.get(cupon = cuponvalid) 
            a = cupon_valid.fechafinal
            b = timezone.now()
            if b < a:
                if cupon_valid.activo  == True:
                    if cupon_valid.cuponusado < cupon_valid.cantidad :
                        cupones = cupon_valid.cuponusado
                        cupones +=1
                        Cupon.objects.filter(cupon = cupon_valid).update(cuponusado= cupones)
                        membresia = cupon_valid.membresia
                        try:
                            em = Empresa.objects.get(nombreEmpresa = empresas.upper())
                            c.empresa = em
                            date = startdate + relativedelta(months=+membresia.duracion)
                            c.fvencimiento = date
                            list = mailchimp.utils.get_connection().get_list_by_id('1ccd0a2ce2')                   
                            try:
                                list.subscribe(c.mail, {'EMAIL':c.mail, 'FNAME': c.nombre, 'LNAME':c.apellido_Paterno})
                                send_mail('Frente', 'Hola '+c.nombre+' '+c.apellido_Paterno+' '+ c.apellido_Materno+' Gracias por suscribirte a La Ciudad de FRENTE, ejemplar quincenal coleccionable que recorre la ciudad de Mexico a partir de sus miles de posibilidades culturales, artisticas, gastronomicas, musicales, de entretenimiento y sus personajes ofreciendote informacion de gran calidad y exclusiva asi como contenido unico en el mercado.  Te confirmamos que ya estas dado de alta y recibiras el proximo numero de FRENTE en la direccion que nos proporcionaste. Para cualquier aclaracion puedes escribirnos a suscripciones@frente.com.mx', 'hola@frente.com.mx', [c.mail], fail_silently=False)
                                c.save()
                                return redirect('clientefrentefinal_list')
                            except Exception, e:
                                ctx = {"form":form, "mensajecupon": "Lo sentimos tu mail ya esta registrado favor de contactarnos en suscripciones@frente.com.mx "}
                                return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                        except Exception, e:
                            print "porque pinches entra aca"
                            c = form.save(commit= False)
                            if empresas == ' ':
                                date = startdate + relativedelta(months=+membresia.duracion)
                                c.fvencimiento = date
                                list = mailchimp.utils.get_connection().get_list_by_id('1ccd0a2ce2')                   
                                try:
                                    list.subscribe(c.mail, {'EMAIL':c.mail, 'FNAME': c.nombre, 'LNAME':c.apellido_Paterno})
                                    send_mail('Frente', 'Hola '+c.nombre+' '+c.apellido_Paterno+' '+ c.apellido_Materno+' Gracias por suscribirte a La Ciudad de FRENTE, ejemplar quincenal coleccionable que recorre la ciudad de Mexico a partir de sus miles de posibilidades culturales, artisticas, gastronomicas, musicales, de entretenimiento y sus personajes ofreciendote informacion de gran calidad y exclusiva asi como contenido unico en el mercado.  Te confirmamos que ya estas dado de alta y recibiras el proximo numero de FRENTE en la direccion que nos proporcionaste. Para cualquier aclaracion puedes escribirnos a suscripciones@frente.com.mx', 'hola@frente.com.mx', [c.mail], fail_silently=False)
                                    c.save()
                                    return redirect('clientefrentefinal_list')
                                except Exception, e:
                                    ctx = {'form':form,'formb': formem, "mensajecupon": "Lo sentimos tu mail ya esta registrado favor de contactarnos en suscripciones@frente.com.mx "}
                                    return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                            else:
                                a = Empresa.objects.create(nombreEmpresa = empresas.upper())
                                a.save()
                                c.empresa = a
                                date = startdate + relativedelta(months=+membresia.duracion)
                                c.fvencimiento = date
                                list = mailchimp.utils.get_connection().get_list_by_id('1ccd0a2ce2')                   
                                try:
                                    list.subscribe(c.mail, {'EMAIL':c.mail, 'FNAME': c.nombre, 'LNAME':c.apellido_Paterno})
                                    send_mail('Frente', 'Hola '+c.nombre+' '+c.apellido_Paterno+' '+ c.apellido_Materno+' Gracias por suscribirte a La Ciudad de FRENTE, ejemplar quincenal coleccionable que recorre la ciudad de Mexico a partir de sus miles de posibilidades culturales, artisticas, gastronomicas, musicales, de entretenimiento y sus personajes ofreciendote informacion de gran calidad y exclusiva asi como contenido unico en el mercado.  Te confirmamos que ya estas dado de alta y recibiras el proximo numero de FRENTE en la direccion que nos proporcionaste. Para cualquier aclaracion puedes escribirnos a suscripciones@frente.com.mx', 'hola@frente.com.mx', [c.mail], fail_silently=False)
                                    c.save()
                                    return redirect('clientefrentefinal_list')
                                except Exception, e:
                                    ctx = {'form':form,'formb': formem, "mensajecupon": "Lo sentimos tu mail ya esta registrado favor de contactarnos en suscripciones@frente.com.mx "}
                                    return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                    else:
                        ctx = {'form':form,'formb': formem, "mensajecupon": "Cupon agotado"}
                    return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                else:
                    ctx = {'form':form,'formb': formem, "mensajecupon": "Cupon Invalido favor de comunicarte con tu proovedor por otro cupon"}
                    return render_to_response(template_name,ctx, context_instance=RequestContext(request))
        except Cupon.DoesNotExist as e: 
            ctx = {'form':form,'formb': formem, "mensajecupon": "El cupon Que Intenta Ingresas No Existe"}
            return render_to_response(template_name,ctx, context_instance=RequestContext(request))
    return render(request, template_name, {'form':form,'formb': formem})

def campania_forid(request, cupon, template_name='frente/frenteregistro.html'):
    startdate = datetime.today()
    try:
        cupones = Cupon.objects.get( cupon = cupon)
        form = CreateClienteCupon(request.POST or None, initial={'cupon': cupones})
        formem = EmpresaForm(request.POST or None, initial={'nombreEmpresa': ' '})
        if form.is_valid() and formem.is_valid():
            cuponvalid= form.cleaned_data['cupon']
            empresas = formem.cleaned_data['nombreEmpresa']
            try:
                cupon_valid = Cupon.objects.get(cupon = cuponvalid) 
                a = cupon_valid.fechafinal
                b = timezone.now()
                if b < a:
                    if cupon_valid.activo  == True:
                        if cupon_valid.cuponusado < cupon_valid.cantidad :
                            cupones = cupon_valid.cuponusado
                            cupones +=1
                            Cupon.objects.filter(cupon = cupon_valid).update(cuponusado= cupones)
                            membresia = cupon_valid.membresia
                            try:
                                em = Empresa.objects.get(nombreEmpresa = empresas.upper())
                                c.empresa = em
                                date = startdate + relativedelta(months=+membresia.duracion)
                                c.fvencimiento = date
                                list = mailchimp.utils.get_connection().get_list_by_id('1ccd0a2ce2')                   
                                try:
                                    list.subscribe(c.mail, {'EMAIL':c.mail, 'FNAME': c.nombre, 'LNAME':c.apellido_Paterno})
                                    send_mail('Frente', 'Hola '+c.nombre+' '+c.apellido_Paterno+' '+ c.apellido_Materno+' Gracias por suscribirte a La Ciudad de FRENTE, ejemplar quincenal coleccionable que recorre la ciudad de Mexico a partir de sus miles de posibilidades culturales, artisticas, gastronomicas, musicales, de entretenimiento y sus personajes ofreciendote informacion de gran calidad y exclusiva asi como contenido unico en el mercado.  Te confirmamos que ya estas dado de alta y recibiras el proximo numero de FRENTE en la direccion que nos proporcionaste. Para cualquier aclaracion puedes escribirnos a suscripciones@frente.com.mx', 'hola@frente.com.mx', [c.mail], fail_silently=False)
                                    c.save()
                                    return redirect('clientefrentefinal_list')
                                except Exception, e:
                                    ctx = {"form":form, "mensajecupon": "Lo sentimos tu mail ya esta registrado favor de contactarnos en suscripciones@frente.com.mx "}
                                    return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                            except Exception, e:
                                c = form.save(commit= False)
                                if empresas == ' ':
                                    date = startdate + relativedelta(months=+membresia.duracion)
                                    c.fvencimiento = date
                                    list = mailchimp.utils.get_connection().get_list_by_id('1ccd0a2ce2')                   
                                    try:
                                        list.subscribe(c.mail, {'EMAIL':c.mail, 'FNAME': c.nombre, 'LNAME':c.apellido_Paterno})
                                        send_mail('Frente', 'Hola '+c.nombre+' '+c.apellido_Paterno+' '+ c.apellido_Materno+' Gracias por suscribirte a La Ciudad de FRENTE, ejemplar quincenal coleccionable que recorre la ciudad de Mexico a partir de sus miles de posibilidades culturales, artisticas, gastronomicas, musicales, de entretenimiento y sus personajes ofreciendote informacion de gran calidad y exclusiva asi como contenido unico en el mercado.  Te confirmamos que ya estas dado de alta y recibiras el proximo numero de FRENTE en la direccion que nos proporcionaste. Para cualquier aclaracion puedes escribirnos a suscripciones@frente.com.mx', 'hola@frente.com.mx', [c.mail], fail_silently=False)
                                        c.save()
                                        return redirect('clientefrentefinal_list')
                                    except Exception, e:
                                        ctx = {'form':form,'formb': formem, "mensajecupon": "Lo sentimos tu mail ya esta registrado favor de contactarnos en suscripciones@frente.com.mx "}
                                        return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                                else:
                                    a = Empresa.objects.create(nombreEmpresa = empresas.upper())
                                    a.save()
                                    c.empresa = a
                                    date = startdate + relativedelta(months=+membresia.duracion)
                                    c.fvencimiento = date
                                    list = mailchimp.utils.get_connection().get_list_by_id('1ccd0a2ce2')                   
                                    try:
                                        list.subscribe(c.mail, {'EMAIL':c.mail, 'FNAME': c.nombre, 'LNAME':c.apellido_Paterno})
                                        send_mail('Frente', 'Hola '+c.nombre+' '+c.apellido_Paterno+' '+ c.apellido_Materno+' Gracias por suscribirte a La Ciudad de FRENTE, ejemplar quincenal coleccionable que recorre la ciudad de Mexico a partir de sus miles de posibilidades culturales, artisticas, gastronomicas, musicales, de entretenimiento y sus personajes ofreciendote informacion de gran calidad y exclusiva asi como contenido unico en el mercado.  Te confirmamos que ya estas dado de alta y recibiras el proximo numero de FRENTE en la direccion que nos proporcionaste. Para cualquier aclaracion puedes escribirnos a suscripciones@frente.com.mx', 'hola@frente.com.mx', [c.mail], fail_silently=False)
                                        c.save()
                                        return redirect('clientefrentefinal_list')
                                    except Exception, e:
                                        ctx = {'form':form,'formb': formem, "mensajecupon": "Lo sentimos tu mail ya esta registrado favor de contactarnos en suscripciones@frente.com.mx "}
                                        return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                        else:
                            ctx = {'form':form,'formb': formem, "mensajecupon": "Cupon agotado"}
                            return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                        ctx = {'form':form,'formb': formem, "mensajecupon": "Algo ocurrio mal podrias recargar la pagína"}
                        return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                    else:
                        ctx = {'form':form,'formb': formem, "mensajecupon": "Cupon Invalido favor de comunicarte con tu proovedor por otro cupon"}
                        return render_to_response(template_name,ctx, context_instance=RequestContext(request))
                else:
                    ctx = {'form':form,'formb': formem, "mensajecupon": "Cupon Invalido favor de comunicarte con tu proovedor por otro cupon"}
                    return render_to_response(template_name,ctx, context_instance=RequestContext(request))
            except Cupon.DoesNotExist as e: 
                ctx = {'form':form,'formb': formem, "mensajecupon": "El cupon Que Intenta Ingresas No Existe"}
                return render_to_response(template_name,ctx, context_instance=RequestContext(request))
        else:
            return render(request, template_name, {'form':form,'formb': formem})
    except Cupon.DoesNotExist: 
        return redirect ('http://www.frente.com.mx/')

class delegacion_ajaxview(TemplateView):

    def get(self, request, *args, **response_kwargs):
        id_delegacion = request.GET ['id']
        colonias = Colonia_frente.objects.filter(delegacion = id_delegacion)
        data = serializers.serialize("json", colonias, fields=('descripcion_Colonia'))
        return HttpResponse(data, content_type="application/json")

@login_required(login_url='/accounts/login/')
def clientefrente_view(request, pk, template_name='frente/clienteview.html'):
    server = get_object_or_404(ClienteFrente, pk=pk)
    viewcliente = ClienteFrente.objects.get( id = pk)
    try:
        pr = Cupon.objects.get( cupon = viewcliente)
        startdate = datetime.today().date()
        a = viewcliente.fvencimiento - relativedelta(months = 1)
        if startdate >= a and startdate <= startdate:
            fecha = True
        else:
            fecha = False
        return render(request, template_name, {'cliente': viewcliente, 'pr': pr, 'fecha': fecha})
    except Exception, e:
        return render(request, template_name, {'cliente': viewcliente})

@login_required(login_url='/accounts/login/')
def clientefrente_update(request, pk, template_name='frente/clientesupdate.html'):
    server = get_object_or_404(ClienteFrente, pk=pk)
    usuario = ClienteFrente.objects.get( id = pk)
    form = updateUser(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('clientefrente_list')
    return render(request, template_name, {'form':form, 'usarios': usuario})

def clientefrente_delete(request, pk, template_name='frente/deletepr.html'):
    server = get_object_or_404(ClienteFrente, pk=pk)    
    if request.method=='POST':
        server.delete()
        return redirect('clientefrente_list')
    return render(request, template_name, {'object':server})

def frente_clientesfinal(request):
    return render_to_response("frente/finalsuscripcion.html")
# Fin de los clientes

# Todo lo que tenga que ver con usuarios de PR
@login_required(login_url='/accounts/login/')
def frente_usuarios(request):
    usuarios = User.objects.filter(groups__name='PR', is_active = True)
    return render_to_response("frente/usuariospr.html",{'usuarios': usuarios}, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def edit_frenteusuarios(request, id, template_name='frente/registropr.html'):
    userpr = get_object_or_404(User, id=id)
    form = updateUserPR(request.POST or None, instance=userpr)
    if form.is_valid():
        form.save()
        return redirect('url_frenteusuarios')
    return render(request, template_name, {'form': form})

def frenteusuarios_delete(request, pk, template_name='frente/deletepr.html'):
    server = get_object_or_404(User, pk=pk)    
    if request.method=='POST':
        server.is_active = False
        server.save()
        return redirect('url_frenteusuarios')
    return render(request, template_name, {'object':server})

@login_required(login_url='/accounts/login/')
def frente(request):
    template = "frente/frente.html"
    return render_to_response(template, context_instance=RequestContext(request))

#############################
### Distribucion o Control###
#############################

class ClieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClieForm, self).__init__(*args, **kwargs)
        self.fields['cumpleanos'].label = 'Cumpleaños'
        self.fields['mail'].label = 'Correo Electrónico'
        self.fields['numero_Exterior'].label = 'Número Exterior'
        self.fields['numero_Interior'].label = 'Número Interior'
        self.fields['cp'].label = 'Código Postal'
        self.fields['delegacion'].label = 'Delegación'
        self.fields['entregas'].label = 'Lugar de Entrega'
        self.fields['cupon'].label = 'Cupón'
        self.fields['phone'].label = 'Teléfono'

    class Meta:
        model = ClienteFrente
        fields = ('nombre','apellido_Paterno','apellido_Materno', 'cumpleanos', 'mail','phone','calle','numero_Exterior','numero_Interior', 'cp','delegacion','Colonia','referencia','entregas','puesto','cupon','dotacion')
        widgets = {'cupon': forms.HiddenInput()}

class QuejaControlForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ('Tipo_queja','Nombre','Correo','Telefono','Queja','id_cliente')
        widgets = {'id_cliente': forms.HiddenInput()}
    

@login_required(login_url='/accounts/login/')
def distribucion(request, template_name = 'distribucion/clientes.html'):
    a = ClienteFrente.objects.filter(activo = True).order_by('apellido_Paterno')
    paginator = Paginator(a, 20)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientes
    return render_to_response(template_name, args, context_instance=RequestContext(request))

def bajaControl(request, pk, template_name='distribucion/bajacliente.html'):
    server = get_object_or_404(ClienteFrente, pk=pk)    
    if request.method=='POST':
        server.is_active = False
        server.save()
        return redirect('distribucion')
    return render(request, template_name, {'object':server})
@login_required(login_url='/accounts/login/')
def searchClienteControl(request, template_name = "distribucion/FilterName.html"):
    k = []
    keyword = request.POST['SearchCliente'].encode("utf-8")
    k = keyword.split(' ') + [keyword]
    argus = {}
    try:
        kwards = {'activo':True}
        args = Q()
        for x in k:
            args.add(Q(nombre__icontains = x)|
                    Q(apellido_Paterno__icontains = x)|
                    Q(apellido_Materno__icontains = x)|
                    Q(empresa__nombreEmpresa__icontains = x), Q.OR)
        ind_list = ClienteFrente.objects.filter(*[args], **kwards)
    except ClienteFrente.DoesNotExist:
        pass
    ########################################################################################################################################
    posts = [{'page':'1'},{'SearchCliente':keyword}]
    ########################################################################################################################################
    if len(ind_list) != 0:
        paginator = Paginator(ind_list, 10)
        page = request.POST.get('page',1)
        try:
            clientesearch = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            clientesearch = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            clientesearch = paginator.page(paginator.num_pages)
        argus['cliente'] = clientesearch
        argus['filtrado'] = keyword
        argus['all_posts'] = posts
    else:
        argus['cliente'] = "No se Encuentra nada"
        argus['filtrado'] = keyword
    return render(request,template_name, argus)

@login_required(login_url='/accounts/login/')
def createClienteContro(request, template_name= "distribucion/createcliente.html"):
    form = ClieForm(request.POST or None, initial={'cupon': "NOCP", 'empresa':"Sin Empresa"})
    formem = EmpresaForm(request.POST or None, initial={'nombreEmpresa': ' '})
    if form.is_valid():
        form.save()
        return redirect('distribucion')
    args = {}
    args['form'] = form
    args['formem'] = formem
    args['texto'] = "Crear Cliente"
    return render(request, template_name, args)

def quejasControl(request, pk, template_name="distribucion/formgenerico.html"):
    cliente = ClienteFrente.objects.get(id = pk)
    if cliente.mail == "SIN_MAIL":
        mail = ""
    else:
        mail = cliente.mail
    if cliente.telefono == 1111:
        telefono = ""
    else:
        telefono = cliente.telefono
    form = QuejaControlForm(request.POST or None, initial={'Nombre': cliente.nombre+" "+cliente.apellido_Paterno,'Correo': mail,'Telefono': telefono, 'id_cliente': cliente.id})
    if form.is_valid():
        print form
        form.save()
        return redirect('distribucion')
    args = {}
    args['form'] = form
    args['texto'] = "Crear Queja"
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def frente_clientes(request):
    clientes = ClienteFrente.objects.all()
    return render_to_response("frente/clientes.html",{'clientes': clientes}, context_instance=RequestContext(request))

#Cupones
@login_required(login_url='/accounts/login/')
def ver_cupones(request):
    cuponactivo = Cupon.objects.all().filter( activo = True )
    cuponinactivo = Cupon.objects.all().filter( activo = False )
    return render_to_response("frente/cuponesview.html",{'cuponactivo': cuponactivo, 'cuponinactivo': cuponinactivo }, context_instance=RequestContext(request))
@login_required(login_url='/accounts/login/')
def register_cupon(request):
    startdate = datetime.today()
    enddate= startdate +  relativedelta(months=+3)
    code = ''.join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for x in range(4)])
    form = CreateCupon(initial={'cupon': code, 'fechafinal':enddate})
    if request.method == "POST":
        form = CreateCupon(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/frente/cupones/')
        else:
            form = CreateCupon()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render_to_response('frente/cupones.html', context)
    else:
        return render(request, 'frente/cupones.html', {'form': form})

@login_required(login_url='/accounts/login/')
def cupon_lista(request, template_name = 'frente/cuponeslistedit.html'):
    servers = Cupon.objects.all().filter( activo = True )
    data = {}
    data['object_list'] = servers
    return render(request, template_name, data)

@login_required(login_url='/accounts/login/')
def cupon_edit(request, pk, template_name='frente/cuponesedit.html'):
    server = get_object_or_404(Cupon, pk=pk)
    viewcupon = Cupon.objects.get( id = pk)
    form = UpdateCupon(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('cupones_lista')
    return render(request, template_name, {'form': form})        
# Terminan los cupones

# Clientes de frente
class CampaniaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaniaForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].label = 'Nombre de la campana'

    class Meta:
        model = Campania
        fields = ('aliado', 'descripcion')

@login_required(login_url='/accounts/login/')
def campania_list(request, template_name='frente/campanias/listcampania.html'):
    servers = Campania.objects.all()
    paginator = Paginator(servers, 20)
    page = request.GET.get('page',1)
    try:
        clientesearch = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientesearch = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientesearch = paginator.page(paginator.num_pages)
    data = {}
    data['object_list'] = clientesearch
    return render(request, template_name, data)

@login_required(login_url='/accounts/login/')
def campania_create(request, template_name='frente/campanias/createcampania.html'):
    form = CampaniaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('campania_list')
    return render(request, template_name, {'form':form})

@login_required(login_url='/accounts/login/')
def campanialist_frente(request, template_name='frente/campanias/listcampania.html'):
    a = Campania.objects.filter(activo = True)
    paginator = Paginator(a, 20)
    page = request.GET.get('page',1)
    try:
        clientesearch = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientesearch = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientesearch = paginator.page(paginator.num_pages)
    args = {}
    args['object_list'] = clientesearch
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def campanialistFalse_frente(request, template_name='frente/campanias/listcampania.html'):
    a = Campania.objects.filter(activo = False)
    paginator = Paginator(a, 20)
    page = request.GET.get('page',1)
    try:
        clientesearch = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientesearch = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientesearch = paginator.page(paginator.num_pages)
    args = {}
    args['object_list'] = clientesearch
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def campania_listaedit(request, template_name = 'frente/campanias/listaedit.html'):
    servers = Campania.objects.all().filter( activo = True )
    data = {}
    data['object_list'] = servers
    return render(request, template_name, data)

@login_required(login_url='/accounts/login/')
def campania_view(request, pk, template_name='frente/campanias/listcampania.html'):
    server = get_object_or_404(ClienteFrente, pk=pk)
    viewcliente = Campania.objects.get( id = pk)
    return render(request, template_name, {'cliente': viewcliente})

@login_required(login_url='/accounts/login/')
def campania_update(request, pk, template_name='frente/campanias/editcampania.html'):
    server = get_object_or_404(Campania, pk=pk)
    usuario = Campania.objects.get( id = pk)
    form = CampaniaForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('campania_list')
    return render(request, template_name, {'form':form, 'usarios': usuario})

@login_required(login_url='/accounts/login/')
def campania_delete(request, pk, template_name='frente/campanias/deletepr.html'):
    server = get_object_or_404(Campania, pk=pk)    
    if request.method=='POST':
        server.delete()
        return redirect('campania_list')
    return render(request, template_name, {'object':server})

# Fin de los clientes

# Aliados de frente

class AliadosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AliadosForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].label = 'Nombre del Aliado'

    class Meta:
        model = Aliados
    
@login_required(login_url='/accounts/login/')
def aliados_list(request, template_name='frente/aliados/listaliados.html'):
    servers = Aliados.objects.all()
    data = {}
    data['object_list'] = servers
    return render(request, template_name, data)

@login_required(login_url='/accounts/login/')
def aliados_create(request, template_name='frente/aliados/createaliados.html'):
    form = AliadosForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('aliados_list')
    return render(request, template_name, {'form':form})

@login_required(login_url='/accounts/login/')
def aliados_listaedit(request, template_name = 'frente/aliados/listedit.html'):
    servers = Aliados.objects.all()
    data = {}
    data['object_list'] = servers
    return render(request, template_name, data)

@login_required(login_url='/accounts/login/')
def aliados_view(request, pk, template_name='frente/aliados/listaliados.html'):
    server = get_object_or_404(Aliados, pk=pk)
    viewcliente = Aliados.objects.get( id = pk)
    return render(request, template_name, {'cliente': viewcliente})

@login_required(login_url='/accounts/login/')
def aliados_update(request, pk, template_name='frente/aliados/editaliados.html'):
    server = get_object_or_404(Aliados, pk=pk)
    # usuario = Aliados.objects.get( id = pk)
    form = AliadosForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('aliados_list')
    return render(request, template_name, {'form':form})

@login_required(login_url='/accounts/login/')
def aliados_delete(request, pk, template_name='frente/aliados/deletepr.html'):
    server = get_object_or_404(Aliados, pk=pk)    
    if request.method=='POST':
        server.delete()
        return redirect('aliados_list')
    return render(request, template_name, {'object':server})

# Fin de los Aliados

#QUEJAS

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ('Tipo_queja','Nombre','Correo','Telefono','Queja')

class SolucionForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ('solucion', 'activada')
        widgets = {'activada': forms.HiddenInput()}
    

def quejas(request, template_name='frente/quejas/quejas.html'):
    form = QuejaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clientefrente_create_new')
    args = {}
    args['form'] = form
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def consulta_quejas(request, queja):
    template_name = ""
    if queja == "1":
        template_name = 'frente/quejas/consuta.html'
    elif queja == "2":
        template_name = 'masxmas/quejasconsulta.html'
    quejas = Queja.objects.filter(activada = True)
    args = {}
    args['queja'] = quejas
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def consulta_quejas_baja(request, queja):
    template_name = ""
    if queja == "1":
        template_name = 'frente/quejas/consuta.html'
    elif queja == "2":
        template_name = 'masxmas/quejasconsulta_baja.html'
    quejas = Queja.objects.filter(activada = False)
    args = {}
    args['queja'] = quejas
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def ver_quejas(request, queja, id):
    template_name = ""
    if queja == "1":
        template_name = 'frente/quejas/ver.html'
    elif queja == "2":
        template_name = 'masxmas/quejaver.html'
    elif queja == "3":
        template_name = 'masxmas/quejaver_solucion.html'
    queja = Queja.objects.get(id = id)
    try:
        cliente = ClienteFrente.objects.get(mail = queja.Correo)
        args = {}
        args['cliente'] = queja
        args['clientefrente'] = cliente
        return render(request, template_name, args)
    except Exception, e:
        args = {}
        args['cliente'] = queja
        # args['clientefrente'] = cliente
        return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def quejas_solucion_masxmas(request, id):
    template_name = 'masxmas/quejassolucion.html'
    queja = Queja.objects.get(id = id)
    form = SolucionForm(request.POST or None, initial = {'activada': False})
    try:
        print 'despues del try'
        cliente = ClienteFrente.objects.filter(Q(mail = queja.Correo) | Q(phone = queja.Telefono) | Q(id = queja.id_cliente))
        print cliente
        if form.is_valid():
            print 'si entro'
            sol = form.cleaned_data['solucion']
            act = form.cleaned_data['activada']
            queja.solucion = sol
            queja.save(update_fields=['solucion'])
            queja.activada = act
            queja.save(update_fields=['activada'])
            return redirect('masxmas')
        args = {}
        args['cliente'] = queja
        args['clientefrente'] = cliente
        args['form'] = form
        return render(request, template_name, args)
    except Exception, e:
        print 'despues de la consulta'
        args = {}
        args['cliente'] = queja
        args['form'] = form
        # args['clientefrente'] = client
        return render(request, template_name, args)

#########
#masxmas#
#########

class masclientesForm(forms.ModelForm):
    class Meta:
        model = ClienteFrente
        fields = ('nombre','apellido_Paterno','apellido_Materno','cumpleanos','phone','mail','calle','cp','numero_Exterior','numero_Interior','Colonia','delegacion','entregas','cupon','empresa','puesto','referencia','rutas','categoria','subcategoria1','subcategoria2','subcategoria3','distribucion','dotacion','ordenentrega','embolsado','activo')
    
@login_required(login_url='/accounts/login/')
def masxmas(request, template_name = "masxmas/clientes.html"):
    cliente = ClienteFrente.objects.filter(activo = True).order_by('apellido_Paterno')
    paginator = Paginator(cliente, 20)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientes
    return render_to_response(template_name, args, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def masxmas_inactivos(request, template_name = "masxmas/clientes_inactivos.html"):
    cliente = ClienteFrente.objects.filter(activo = False).order_by('apellido_Paterno')
    paginator = Paginator(cliente, 20)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientes
    return render_to_response(template_name, args, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def clientesnuevos(request, template_name = "masxmas/clientesnuevos.html"):
    newc = ClienteFrente.objects.filter(ordenentrega = None).order_by('-created')
    paginator = Paginator(newc, 10)
    page = request.GET.get('page',1)
    try:
        newcliente = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        newcliente = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        newcliente = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = newcliente
    return render(request,template_name, args)

@login_required(login_url='/accounts/login/')
def ShowCliente(request, id, template_name = "masxmas/showcliente.html"):
    server = get_object_or_404(ClienteFrente, id=id)
    viewcliente = ClienteFrente.objects.get( id = id)
    args = {}
    args['cliente'] = viewcliente
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def edit_clientesmasxmas(request, id, template_name = "masxmas/edit_user.html"):
    server = get_object_or_404(ClienteFrente, id=id)
    form = masclientesForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('masxmas')
    args = {}
    args['form'] = form
    args['texto'] = "Agregando los campso del usuario "
    args['cliente'] = server
    return render(request, template_name, args)

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
    

@login_required(login_url='/accounts/login/')
def rutas_new(request, template_name = "masxmas/formgenerico.html"):
    form = RutaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rutas_list')
    args = {}
    args['form'] = form
    args['texto'] = "Agregar una nueva ruta"
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def rutas_list(request, template_name = "masxmas/rutas_list.html"):
    rutas = Ruta.objects.all().order_by('descripcion_Ruta')
    paginator = Paginator(rutas, 10)
    page = request.GET.get('page',1)
    try:
        ruta = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ruta = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ruta = paginator.page(paginator.num_pages)
    args = {}
    args['texto'] = "Listado de Rutas"
    args['rutas'] = ruta
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def rutas_edit(request, id, template_name = "masxmas/formgenerico.html"):
    server = get_object_or_404(Ruta, id=id)
    form = RutaForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('masxmas')
    args = {}
    args['form'] = form
    args['texto'] = "Modificando la ruta "+ server.descripcion_Ruta
    args['cliente'] = server
    return render(request, template_name, args)


# REPARTIDOR

class RepartidorForm(forms.ModelForm):
     class Meta:
         model = Repartidor

@login_required(login_url='/accounts/login/')
def reportidores_list(request, template_name = "masxmas/repartidores_list.html"):
    repa = Repartidor.objects.all().order_by('rutas')
    paginator = Paginator(repa, 10)
    page = request.GET.get('page',1)
    try:
        rutas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rutas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rutas = paginator.page(paginator.num_pages)
    args = {}
    args['repa'] = rutas
    return render (request, template_name, args)

@login_required(login_url='/accounts/login/')
def repartidor_edit(request, id, template_name = "masxmas/formgenerico.html"):
    server = get_object_or_404(Repartidor, id=id)
    form = RepartidorForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('reportidores_list')
    args = {}
    args['form'] = form
    args['texto'] = "Modificando el Repartidor "+ server.nombre +" "+ server.apellido_Paterno+" "+ server.apellido_Materno
    args['cliente'] = server
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def repartidor_new(request, template_name = "masxmas/formgenerico.html"):
    form = RepartidorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rutas_list')
    args = {}
    args['form'] = form
    args['texto'] = "Agregar un nuevo repartidor"
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def repartidor_ver(request, id, template_name = 'masxmas/repatidorver.html'):
    clientes = ClienteFrente.objects.filter(rutas = id).order_by('ordenentrega')

    total_adi = ClienteFrente.objects.filter(rutas = id).aggregate(Sum('adicional'))
    total_adi = u'%s' % (total_adi['adicional__sum'])

    print total_adi

    total_dot = ClienteFrente.objects.filter(rutas = id).aggregate(Sum('dotacion'))
    total_dot = u'%s' % (total_dot['dotacion__sum'])

    print total_dot

    total_tot = ClienteFrente.objects.filter(rutas = id).aggregate(Sum('total'))
    total_tot = u'%s' % (total_tot['total__sum'])

    print total_tot

    paginator = Paginator(clientes, 25)
    page = request.GET.get('page',1)
    try:
        rutas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rutas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rutas = paginator.page(paginator.num_pages)
    args = {}
    args['rutas'] = rutas
    args['valor'] = id
    args['total_adi'] = total_adi
    args['total_dot'] = total_dot
    args['total_tot'] = total_tot
    return render_to_response(template_name, args)

@login_required(login_url='/accounts/login/')
def changeDotacion(request):
    id = request.GET.get('id', None)
    dotacion = request.GET.get('dotacion', None)
    t = ClienteFrente.objects.get(id = id)
    tf = t.dotacion
    tf = int(dotacion) - int(tf)
    ClienteFrente.objects.filter(id = id).update(adicional = dotacion)
    ClienteFrente.objects.filter(id = id).update(total = tf)

    ruta = request.GET.get('rutas', None)

    total_adi = ClienteFrente.objects.filter(rutas = ruta).aggregate(Sum('adicional'))
    total_adi = u'%s' % (total_adi['adicional__sum'])

    print total_adi

    total_tot = ClienteFrente.objects.filter(rutas = ruta).aggregate(Sum('total'))
    total_tot = u'%s' % (total_tot['total__sum'])

    print total_tot

    print tf
    data = []
    data.append({'tf':tf, 'total_adi':total_adi, 'total_tot':total_tot})
    return HttpResponse(simplejson.dumps(data), content_type = 'application/json')

# CATEGORIA

class CategoriaForm(forms.ModelForm):
     class Meta:
         model = Categoria

@login_required(login_url='/accounts/login/')
def categoria_list(request, template_name = "masxmas/categoria_list.html"):
    categoria = Categoria.objects.all()
    args = {}
    args['cate'] = categoria
    return render (request, template_name, args)

@login_required(login_url='/accounts/login/')
def categoria_edit(request, id, template_name = "masxmas/formgenerico.html"):
    server = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('categoria_list')
    args = {}
    args['form'] = form
    args['texto'] = "Modificando el categoria "+ server.descripcion_Categoria
    args['cliente'] = server
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def categoria_new(request, template_name = "masxmas/formgenerico.html"):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rutas_list')
    args = {}
    args['form'] = form
    args['texto'] = "Agregar una nueva Categoria"
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def categoria_filter(request, id, template_name = "masxmas/filter.html"):
    server = get_object_or_404(Categoria, id=id)
    filtro = ClienteFrente.objects.filter(categoria = server)
    paginator = Paginator(filtro, 10)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientes
    args['filtrado'] = server
    return render_to_response(template_name,args)

# SUBCATEGORIA 1

class Subcategoria1Form(forms.ModelForm):
     class Meta:
         model = Subcategoria1

@login_required(login_url='/accounts/login/')
def subcategoria1_list(request, template_name = "masxmas/subcategorias_list.html"):
    subcate1 = Subcategoria1.objects.all().order_by('descripcion_SubCategoria1')
    paginator = Paginator(subcate1, 10)
    page = request.GET.get('page',1)
    try:
        sub1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sub1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sub1 = paginator.page(paginator.num_pages)
    args = {}
    args['subcate'] = sub1
    args['texto'] = "Sub Categoria 1"
    return render (request, template_name, args)
@login_required(login_url='/accounts/login/')
def subcategoria1_edit(request, id, template_name = "masxmas/formgenerico.html"):
    server = get_object_or_404(Subcategoria1, id=id)
    form = Subcategoria1Form(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('subcategoria1_list')
    args = {}
    args['form'] = form
    args['texto'] = "Modificando la SubCategoria "+ server.descripcion_SubCategoria1
    args['cliente'] = server
    return render(request, template_name, args)
@login_required(login_url='/accounts/login/')
def subcategoria1_new(request, template_name = "masxmas/formgenerico.html"):
    form = Subcategoria1Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rutas_list')
    args = {}
    args['form'] = form
    args['texto'] = "Agregar una nueva SubCategoria 1"
    return render(request, template_name, args)
@login_required(login_url='/accounts/login/')
def subcategoria1_filter(request, id, template_name = "masxmas/filter.html"):
    server = get_object_or_404(Subcategoria1, id=id)
    print server
    filtro = ClienteFrente.objects.filter(subcategoria1 = server).order_by('apellido_Paterno')
    paginator = Paginator(filtro, 20)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientes
    args['filtrado'] = server
    return render_to_response(template_name,args)

# SUBCATEGORIA 2

class Subcategoria2Form(forms.ModelForm):
     class Meta:
         model = Subcategoria2
@login_required(login_url='/accounts/login/')
def subcategoria2_list(request, template_name = "masxmas/subcategorias_list.html"):
    subcate2 = Subcategoria2.objects.all().order_by('descripcion_SubCategoria2')
    paginator = Paginator(subcate2, 10)
    page = request.GET.get('page',1)
    try:
        sub2 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sub2 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sub2 = paginator.page(paginator.num_pages)
    args = {}
    args['subcate'] = sub2
    args['texto'] = "Sub Categoria 2"
    return render (request, template_name, args)

@login_required(login_url='/accounts/login/')
def subcategoria2_edit(request, id, template_name = "masxmas/formgenerico.html"):
    server = get_object_or_404(Subcategoria2, id=id)
    form = Subcategoria2Form(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('subcategoria2_list')
    args = {}
    args['form'] = form
    args['texto'] = "Modificando el Subcategoria "+ server.descripcion_SubCategoria2
    args['cliente'] = server
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def subcategoria2_new(request, template_name = "masxmas/formgenerico.html"):
    form = Subcategoria2Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rutas_list')
    args = {}
    args['form'] = form
    args['texto'] = "Agregar una nueva SubCategoria 2"
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def subcategoria2_filter(request, id, template_name = "masxmas/filter.html"):
    server = get_object_or_404(Subcategoria2, id=id)
    filtro = ClienteFrente.objects.filter(subcategoria2 = server)
    paginator = Paginator(filtro, 20)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientes
    args['filtrado'] = server
    return render_to_response(template_name,args)

# SUBCATEGORIA 3

class Subcategoria3Form(forms.ModelForm):
     class Meta:
         model = Subcategoria3

@login_required(login_url='/accounts/login/')
def subcategoria3_list(request, template_name = "masxmas/sub3.html"):
    subcate3 = Subcategoria3.objects.all().order_by('descripcion_SubCategoria3')
    paginator = Paginator(subcate3, 10)
    page = request.GET.get('page',1)
    try:
        sub3 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sub3 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sub3 = paginator.page(paginator.num_pages)
    args = {}
    args['subcate'] = sub3
    args['texto'] = "Sub Categoria 3"
    return render(request,template_name, args)

@login_required(login_url='/accounts/login/')
def subcategoria3_edit(request, id, template_name = "masxmas/formgenerico.html"):
    server = get_object_or_404(Subcategoria3, id=id)
    form = Subcategoria3Form(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('subcategoria3_list')
    args = {}
    args['form'] = form
    args['texto'] = "Modificando el Subcategoria "+ server.descripcion_SubCategoria3
    args['cliente'] = server
    return render(request, template_name, args)
@login_required(login_url='/accounts/login/')
def subcategoria3_new(request, template_name = "masxmas/formgenerico.html"):
    form = Subcategoria3Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rutas_list')
    args = {}
    args['form'] = form
    args['texto'] = "Agregar una nueva SubCategoria 3"
    return render(request, template_name, args)
@login_required(login_url='/accounts/login/')
def subcategoria3_filter(request, id, template_name = "masxmas/filter.html"):
    server = get_object_or_404(Subcategoria3, id=id)
    filtro = ClienteFrente.objects.filter(subcategoria3 = server)
    paginator = Paginator(filtro, 20)
    page = request.GET.get('page',1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientes
    args['filtrado'] = server
    return render_to_response(template_name,args)

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporteclientes.csv"'
    a =ClienteFrente.objects.all()


    writer = csv.writer(response)
    writer.writerow([
        (u"Categoria"),
        (u"subcategoria1"),
        (u"subcategoria3"),
        (u"Ruta"),
        (u"Nombre de la Empresa"),
        (u"Calle"),
        (u"Numero Exterior"),
        (u"Numero Interior"),
        (u"Colonia"),
        (u"Codigo Postal"),
        (u"Delegacion"),
        (u"Referencia de Entrega"),
        (u"Nombre"),
        (u"apellido Paterno"),
        (u"Apellido Materno"),
        (u"Puesto"),
        (u"entregas"),
        (u"Telefono"),
        (u"Correo"),
    ])
    for g in a:
        writer.writerow([g.nombre,g.apellido_Paterno,g.apellido_Materno,g.telefono,g.mail,g.calle,g.numero_Exterior,g.numero_Interior,g.cp,g.Colonia,g.delegacion,g.entregas,g.rutas,g.categoria,g.subcategoria1,g.subcategoria2,g.subcategoria3])

    return response

######
##PR##
######
class CuponPRForm(forms.ModelForm):
    cupon =  forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
    class Meta:
        model = Cupon
        fields = ('cupon', 'cantidad','mail_cliente', 'fechafinal', 'usuariogen', 'membresia')
        widgets = {'fechafinal': forms.HiddenInput(), 'membresia': forms.HiddenInput(), 'cantidad': forms.HiddenInput(), 'usuariogen': forms.HiddenInput()}
    

@login_required(login_url='/accounts/login/')
def pr(request, template_name = "pr/cupon.html"):
    startdate = datetime.today()
    enddate= startdate +  relativedelta(months=+3)
    code = ''.join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for x in range(4)])
    form = CuponPRForm(request.POST or None, initial={'cupon': code, 'fechafinal':enddate, 'membresia': 2, 'cantidad': 1, 'usuariogen': request.user.id})
    if form.is_valid():
        cuponv= form.cleaned_data['cupon']
        mail= form.cleaned_data['mail_cliente']
        send_mail('Membresia Gratis', ' Bienvenido a La Ciudad de FRENTE, ejemplar quincenal coleccionable que recorre la ciudad de Mexico a partir de sus miles de posibilidades culturales, artisticas, gastronomicas, musicales, de entretenimiento y sus personajes ofreciendote informacion de gran calidad y exclusiva asi como contenido unico en el mercado. Te confirmamos que ya esta dado de alta tu cupon y listo para ser canjeable en URL. http://suscripciones.frente.com.mx/promocion/'+cuponv+' \n Para cualquier aclaracion puedes escribirnos a suscripciones@frente.com.mx \nEsperamos que disfrutes de tus ejemplares \n www.frente.com.mx \n www.facebook.com/frentemx \n @FrenteMx', 'hola@frente.com.mx', [mail], fail_silently=False)
        form.save()
        return redirect('pr_cupones_ver')
    args = {}
    args['form'] = form
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def pr_cupones_ver(request, template_name = 'pr/ver_cupones.html'):
    cupones = Cupon.objects.filter(usuariogen = request.user.id)
    args = {}
    args['cupones'] = cupones
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')    
def rutas_export(request, id):
    startdate = date.today()
    # Create the HttpResponse object with the appropriate CSV header.
    a = ClienteFrente.objects.filter(rutas__repartidor__rutas = id).order_by('ordenentrega')
    repa = a[0].rutas.repartidor_set.get()
    nombre = a[0].rutas.descripcion_Ruta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+nombre+'_'+str(startdate)+'.csv"'

    writer = csv.writer(response)
    writer.writerow([
        (u"REPARTIDOR"),
        (u"RUTA"),
        (u"FECHA"),
        ])
    writer.writerow([
        (repa.nombre+" "+repa.apellido_Paterno), a[0].rutas.numero_Ruta, str(startdate)
        ])
    writer.writerow([
        (u"CONCECPTO"),
        (u"RUTA"),
        (u"REPARTIDOR"),
        (u"CUENTA"),
        (u"DIRECCION CLIENTE DIRECTO"),
        (u"NUMERO INTERIOR"),
        (u"NUMERO EXTERIOR"),
        (u"COLONIA"),
        (u"DELEGACION"),
        (u"CONTACTO DIRECTO"),
        (u"APELLIDO PATERNO"),
        (u"DOTACION"),
        (u"OBSERVACIONES"),

    ])
    for g in a:
        writer.writerow([g.subcategoria3,("RUTA ",g.rutas.numero_Ruta),(repa.nombre+" "+repa.apellido_Paterno),g.empresa,smart_bytes(g.calle, encoding='utf-8', strings_only=False, errors='strict'),g.numero_Exterior,g.numero_Interior,g.Colonia,g.delegacion,g.nombre,smart_bytes(g.apellido_Paterno, encoding='utf-8', strings_only=False, errors='strict'),g.dotacion,"NOMBRE Y FIRMA"])

    return response

def clientesparse(request):
    count = 0
    filesource = '/home/data4/myenv/frente-subscripciones/prueba1.csv'
    with open(filesource, 'rb') as f:
        reader = csv.reader(f, delimiter = ',', quotechar='"')
        reader.next()
        for line in reader:
            distribucion = line[0]
            categoria = line[1]
            subcategoria1 = line[2]
            subcategoria2 = line[3]
            subcategoria3 = line[4]
            ordenentrega = line[5]
            ruta = line[7]
            empresa = line[9]
            entregas = line[10]
            calle = line[12]
            numeroexterno = line[13]
            numerointerno = line[14]
            colonia = line[15]
            cp = line[16]
            delegacion = line[18]
            referencia = line[19]
            nombre = line[20]
            aparterno = line[21]
            amaterno = line[22]
            puesto = line[23]
            dotacion = line[25]
            embolsado = line[26]
            cumpleanos = line[28]
            telefono = line[29]
            mail = line[30]
            cupon = line[31]
            activo = line[32]
            fvencimiento = line[33]
            ordenentrega = int(ordenentrega)
            # numeroexterno = int(numeroexterno)
            dotacion = int(dotacion)
            if  cumpleanos == '':
                cumpleanos = '2020-06-19'
            if  fvencimiento == '':
                fvencimiento = '2020-06-19'
            if  activo == '':
                activo = "t"
            if  nombre == '':
                nombre = "NONAME"
            if amaterno == '':
                amaterno = "NONAME"
            if aparterno == '':
                aparterno = "NONAME"
            if embolsado == '':
                embolsado = "NO APLICA"
            if entregas == "TRABAJA":
                entregas = "oficina"
            elif entregas == "VIVE":
                entregas = "casa"
            else:
                entregas = "oficina"
            if  telefono == '':
                telefono = 1111
            if  cupon == '':
                cupon = "NOCP"
            if  mail == '':
                mail = "SIN_MAIL"
            if  puesto == '':
                puesto = "SIN_PUESTO"
            if cp == '':
                cp = 111111
            if numeroexterno == 'S/N':
                numeroexterno = 0
            numeroexterno = int(numeroexterno)
            sub1 = Subcategoria1.objects.get(descripcion_SubCategoria1 = subcategoria1)
            subcategoria1 = sub1
            sub2 = Subcategoria2.objects.get(descripcion_SubCategoria2 = subcategoria2)
            subcategoria2 = sub2
            sub3 = Subcategoria3.objects.get(descripcion_SubCategoria3 = subcategoria3)
            subcategoria3 = sub3
            dele = Delegacion_frente.objects.filter(descripcion_Delegacion = delegacion.title())
            delegacion = dele[0]
            col = Colonia_frente.objects.get(descripcion_Colonia = colonia, delegacion = delegacion )
            colonia = col
            rutas = Ruta.objects.get(descripcion_Ruta = ruta)
            ruta = rutas
            categorias = Categoria.objects.get(descripcion_Categoria = categoria)
            categoria = categorias
            empresas = Empresa.objects.get(nombreEmpresa = empresa)
            empresa = empresas
            controladas = Canal_distribucion.objects.get(descripcion_Distribucion = distribucion)
            distribucion = controladas
            print nombre,amaterno,aparterno,cumpleanos,telefono,mail,calle,cp,numeroexterno,numerointerno,colonia,delegacion,entregas,cupon,empresa,puesto,referencia,fvencimiento,activo,ruta,categoria,subcategoria1,subcategoria2,subcategoria3,dotacion,ordenentrega,embolsado
            ClienteFrente.objects.create(nombre = nombre,apellido_Paterno = aparterno,apellido_Materno = amaterno,cumpleanos = cumpleanos,telefono = telefono,mail = mail,calle = calle,cp = cp,numero_Exterior = numeroexterno,numero_Interior = numerointerno,Colonia = col,delegacion = delegacion,entregas = entregas,cupon = cupon,empresa = empresa,puesto = puesto,referencia = referencia,fvencimiento = fvencimiento,activo = activo,rutas = ruta,categoria = categoria,subcategoria1 = subcategoria1,subcategoria2 = subcategoria2,subcategoria3 = subcategoria3,distribucion = distribucion,dotacion = dotacion ,ordenentrega = ordenentrega,embolsado = embolsado)
            count = count+1
    return redirect('/')

def parsedele(request):
    filesource = '/home/servicio/python/dele.csv'
    with open(filesource, 'rb') as f:
        reader = csv.reader(f, delimiter = ',', quotechar='"')
        reader.next()
        for line in reader:
            dele = line[0]
            Delegacion_frente.objects.create(descripcion_Delegacion = dele)
    return redirect('/')

def parsecol(request):
    filesource = '/home/servicio/python/col.csv'
    with open(filesource, 'rb') as f:
        reader = csv.reader(f, delimiter = ',', quotechar='"')
        reader.next()
        for line in reader:
            col = line[0]
            delegacion = line[1]
            dele = Delegacion_frente.objects.filter(descripcion_Delegacion = delegacion)
            delegacio = dele[0]
            Colonia_frente.objects.create(descripcion_Colonia = col,delegacion = delegacio )
    return redirect('/')

def parsempe(request):
    filesource = '/home/servicio/python/empe.csv'
    with open(filesource, 'rb') as f:
        reader = csv.reader(f, delimiter = ',', quotechar='"')
        reader.next()
        for line in reader:
            empe = line[0]
            Empresa.objects.create(nombreEmpresa = empe)
    return redirect('/')

def parserutas(request):
    filesource = '/home/servicio/python/rutas.csv'
    with open(filesource, 'rb') as f:
        reader = csv.reader(f, delimiter = ',', quotechar='"')
        reader.next()
        for line in reader:
            num = line[0]
            ruta = line[1]
            Ruta.objects.create(numero_Ruta = num, descripcion_Ruta = ruta)
    return redirect('/')

def pasrsesub3(request):
    filesource = '/home/servicio/python/sub3.csv'
    with open(filesource, 'rb') as f:
        reader = csv.reader(f, delimiter = ',', quotechar='"')
        reader.next()
        for line in reader:
            empe = line[0]
            Subcategoria3.objects.create(descripcion_SubCategoria3 = empe)
    return redirect('/')

def parserepa(request):
    filesource = '/home/servicio/python/repas.csv'
    with open(filesource, 'rb') as f:
        reader = csv.reader(f, delimiter = ',', quotechar='"')
        reader.next()
        for line in reader:
            nom = line[0]
            ap = line[1]
            am = line[2]
            ruta = line[3]
            rutas = Ruta.objects.get(descripcion_Ruta =ruta)
            Repartidor.objects.create(nombre = nom, apellido_Paterno = ap,apellido_Materno = am,rutas=rutas)
    return redirect('/')
@login_required(login_url='/accounts/login/')
def searchCliente(request, template_name = "masxmas/filtername.html"):
    if not request.POST:
        argus = {}
        argus['cliente'] = "No se Encuentra nada"
        argus['filtrado'] = "No se Econtro Nada"
        return render(request,template_name, argus)
    k = []
    keyword = request.POST['SearchCliente'].encode("utf-8")
    print "Esto es keyword",keyword
    k = keyword.split(' ') + [keyword]
    argus = {}
    try:
        kwards = {}
        args = Q()
        for x in k:
            args.add(Q(nombre__icontains = x)|
                    Q(apellido_Paterno__icontains = x)|
                    Q(apellido_Materno__icontains = x)|
                    Q(empresa__nombreEmpresa__icontains = x), Q.OR)
        ind_list = ClienteFrente.objects.filter(*[args], **kwards)
    except ClienteFrente.DoesNotExist:
        pass
    ########################################################################################################################################
    posts = [{'page':'1'},{'SearchCliente':keyword}]
    ########################################################################################################################################
    if len(ind_list) != 0:
        paginator = Paginator(ind_list, 10)
        page = request.POST.get('page',1)
        try:
            clientesearch = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            clientesearch = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            clientesearch = paginator.page(paginator.num_pages)
        argus['cliente'] = clientesearch
        argus['filtrado'] = keyword
        argus['all_posts'] = posts
    else:
        argus['cliente'] = "No se Encuentra nada"
        argus['filtrado'] = keyword
    return render(request,template_name, argus)


#####################
##CAMPANIAS MASXMAS##
#####################
@login_required(login_url='/accounts/login/')
def campanialist(request, template_name='masxmas/listcampania.html'):
    a = Campania.objects.filter(activo = True)
    paginator = Paginator(a, 20)
    page = request.GET.get('page',1)
    try:
        clientesearch = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientesearch = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientesearch = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientesearch
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def campanialistFalse(request, template_name='masxmas/listcampania.html'):
    a = Campania.objects.filter(activo = False)
    paginator = Paginator(a, 20)
    page = request.GET.get('page',1)
    try:
        clientesearch = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientesearch = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientesearch = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientesearch
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def clientescupones(request, cupon, template_name = "masxmas/clientes_campanas.html"):
    clientes = ClienteFrente.objects.filter(cupon = cupon)
    cupons = Cupon.objects.get(cupon = cupon)
    paginator = Paginator(clientes, 20)
    page = request.GET.get('page',1)
    try:
        clientesearch = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientesearch = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientesearch = paginator.page(paginator.num_pages)
    args = {}
    args['cliente'] = clientesearch
    args['filtrado'] = cupons.campania
    args['cupon'] = cupon
    return render(request, template_name, args)

@login_required(login_url='/accounts/login/')
def desactivar_campana(request, cupon, template_name = "masxmas/listcampania.html"):
    ClienteFrente.objects.filter(cupon = cupon).update(activo = False)
    return redirect('/distribucion/campania/activa')

@login_required(login_url='/accounts/login/')
def export_info(request, nr):

    nr = nr.encode("utf-8")
    nr = int(nr)
    info = ' '
    last = 0

    clientes = ClienteFrente.objects.filter(rutas = nr).distinct('calle','numero_Exterior','empresa','ordenentrega').order_by('ordenentrega')
    repartidores = Repartidor.objects.filter(rutas = nr)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

    url = SITE_ROOT + ('/static/img/Frente_titulo.jpg')

    output = StringIO.StringIO()

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('hojas_reparto')

    format = workbook.add_format()

    format.set_pattern(1)  # This is optional when using a solid fill.
    format.set_bg_color('#8497B0')
    format.set_bold()
    format.set_font_size(12)
    format.set_align('center')
    format.set_align('vcenter')
    format.set_text_wrap()
    format.set_border()
    format.set_font_name('Arial')

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 5)
    worksheet.write(7, 0, '# ENT', format)

    worksheet.set_column('B:B', 30)
    worksheet.write(7, 1, 'CONCEPTO', format)

    worksheet.set_column('C:C', 10)
    worksheet.write(7, 2, 'RUTA', format)

    worksheet.set_column('D:D', 20)
    worksheet.write(7, 3, 'REPARTIDOR', format)

    worksheet.set_column('E:E', 50)
    worksheet.write(7, 4, 'NOMBRE DE LA EMPRESA', format)

    worksheet.set_column('F:F', 70)
    worksheet.write(7, 5, 'DIRECCION CLIENTE DIRECTO', format)

    worksheet.set_column('G:G', 30)
    worksheet.write(7, 6, 'COLONIA', format)

    worksheet.set_column('H:H', 25)
    worksheet.write(7, 7, 'DELEGACION', format)

    worksheet.set_column('I:I', 30)
    worksheet.write(7, 8, 'CONTACTO DIRECTO 1', format)

    worksheet.set_column('J:J', 10)
    worksheet.write(7, 9, 'TIPO DE RACK', format)

    worksheet.set_column('K:K', 3)
    worksheet.write(7, 10, '#', format)

    worksheet.set_column('L:L', 15)
    worksheet.write(7, 11, 'DOTACIÓN', format)

    worksheet.set_column('M:M', 50)
    worksheet.write(7, 12, 'OBSERVACIONES', format)

    worksheet.set_row(7, 29.9)

    format = workbook.add_format()

    format.set_pattern(1)
    format.set_font_size(14)
    format.set_bg_color('white')
    format.set_align('center')
    format.set_align('vcenter')
    format.set_text_wrap()
    format.set_border()
    format.set_font_name('Arial')

    format0 = workbook.add_format()

    format0.set_pattern(1)
    format0.set_font_size(14)
    format0.set_bg_color('white')
    format0.set_align('left')
    format0.set_align('vcenter')
    format0.set_text_wrap()
    format0.set_border()
    format0.set_font_name('Arial')
    format0.set_bold()

    format1 = workbook.add_format()

    format1.set_pattern(1)
    format1.set_font_size(12)
    format1.set_bg_color('white')
    format1.set_align('center')
    format1.set_align('bottom')
    format1.set_text_wrap()
    format1.set_border()

    format2 = workbook.add_format()

    format2.set_pattern(1)
    format2.set_font_size(24)
    format2.set_bg_color('white')
    format2.set_align('right')
    format2.set_align('vcenter')

    format3 = workbook.add_format()

    format3.set_pattern(1)
    format3.set_font_size(24)
    format3.set_bg_color('white')
    format3.set_align('center')
    format3.set_align('vcenter')

    format4 = workbook.add_format()

    format4.set_pattern(1)
    format4.set_font_size(14)
    format4.set_bg_color('white')
    format4.set_align('center')
    format4.set_align('vcenter')
    format4.set_text_wrap()
    format4.set_border()
    format4.set_font_name('Arial')
    format4.set_bold()

    worksheet.merge_range('I2:J2', 'REPARTIDOR:', format2)
    worksheet.merge_range('I3:J3', 'RUTA:', format2)
    worksheet.merge_range('I4:J4', 'FECHA:', format2)

    info = u'%s %s' % (repartidores[0].nombre, repartidores[0].apellido_Paterno)
    worksheet.merge_range('L2:M2', info, format3)
    info = u'%s' % (nr)
    worksheet.merge_range('L3:M3', info, format3)
    info = datetime.today().date()
    info = u'%s' % (info)
    worksheet.merge_range('L4:M4', info, format3)
    
    worksheet.set_row(1, 35)
    worksheet.set_row(2, 35)
    worksheet.set_row(3, 35)

    for i in range(0, len(clientes)):

        t1 = clientes[i].empresa.clientefrente_set.filter(rutas = nr).distinct().count()
        t1 = u'%s' % (t1)
        t2 = clientes[i].empresa.clientefrente_set.filter(rutas = nr).aggregate(Sum('adicional'))
        t2 = u'%s' % (t2['adicional__sum'])

        info = clientes[i].ordenentrega
        info = str(info)
        worksheet.write(i+8, 0, info, format)
        worksheet.set_row(i+8, 80)

        info = clientes[i].subcategoria1
        info = u'%s' % (info)
        worksheet.write(i+8, 1, info, format)
        worksheet.set_row(i+8, 80)

        info = 'RUTA ' + str(nr)
        worksheet.write(i+8, 2, info, format)
        worksheet.set_row(i+8, 80)

        info = u'%s %s' % (repartidores[0].nombre, repartidores[0].apellido_Paterno)
        worksheet.write(i+8, 3, info, format)
        worksheet.set_row(i+8, 80)

        info = u'%s' % (clientes[i].empresa)
        worksheet.write(i+8, 4, info, format0)
        worksheet.set_row(i+8, 80)

        info = u'%s %s' % (clientes[i].calle, clientes[i].numero_Exterior)
        worksheet.write(i+8, 5, info, format0)
        worksheet.set_row(i+8, 80)

        info = u'%s' % (clientes[i].Colonia)
        worksheet.write(i+8, 6, info, format)
        worksheet.set_row(i+8, 80)

        info = u'%s' % (clientes[i].delegacion)
        worksheet.write(i+8, 7, info, format)
        worksheet.set_row(i+8, 80)

        info = u'%s %s' % (clientes[i].nombre, clientes[i].apellido_Paterno)
        worksheet.write(i+8, 8, info, format0)
        worksheet.set_row(i+8, 80)

        worksheet.write(i+8, 9, ' ', format)
        worksheet.set_row(i+8, 80)

        worksheet.write(i+8, 10, t1, format)
        worksheet.set_row(i+8, 80)

        worksheet.write(i+8, 11, t2, format4)
        worksheet.set_row(i+8, 80)

        worksheet.write(i+8, 12, 'NOMBRE Y FIRMA O SELLO', format1)
        worksheet.set_row(i+8, 80)
        j = i + 1

    j = j + 8

    format5 = workbook.add_format()

    format5.set_pattern(1)
    format5.set_font_size(20)
    format5.set_bg_color('black')
    format5.set_align('center')
    format5.set_align('vcenter')
    format5.set_font_color('white')
    format5.set_bold()

    worksheet.set_row(j, 30)
    info = ClienteFrente.objects.filter(rutas = nr).aggregate(Sum('adicional'))
    info = u'%s' % (info['adicional__sum'])
    j += 1
    j = str(j)
    worksheet.merge_range('I'+j+':J'+j, 'TOTAL:', format5)
    worksheet.merge_range('K'+j+':L'+j, info, format5)

    worksheet.insert_image('A1', url, {'x_offset': 0, 'y_offset': 0, 'x_scale': 1, 'y_scale': 1})
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=hojas_reparto.xlsx"

    return response

def tags(request, nr):
    nr = nr.encode("utf-8")
    nr = int(nr)
    info = ' '

    clientes = ClienteFrente.objects.filter(rutas = nr).order_by('ordenentrega')
    repartidores = Repartidor.objects.filter(rutas = nr)

    output = StringIO.StringIO()

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('etiquetas')

    format = workbook.add_format()

    format.set_pattern(1)
    format.set_bold()
    format.set_bg_color('white')
    format.set_font_size(8)
    format.set_align('center')
    format.set_align('vcenter')
    format.set_text_wrap()
    format.set_border(0)

    j = 0
    k = 0

    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 0.5)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 0.5)
    worksheet.set_column('E:E', 30)

    for i in range(0, len(clientes)):
        if j > 2:
            j = 0
            k += 1
            info = u"FRENTE/ %s_%s AT'N: %s %s (%s) RUTA %s_%s DIR: %s %s %s %s DOT: %s %s" % (clientes[i].subcategoria3,
                                                                              clientes[i].empresa,
                                                                              clientes[i].nombre,
                                                                              clientes[i].apellido_Paterno,
                                                                              clientes[i].puesto,
                                                                              nr,
                                                                              clientes[i].ordenentrega,
                                                                              clientes[i].calle,
                                                                              clientes[i].numero_Exterior,
                                                                              clientes[i].numero_Interior,
                                                                              clientes[i].referencia,
                                                                              clientes[i].adicional,
                                                                              clientes[i].day)
            worksheet.write(k, j*2, info, format)
            worksheet.write(k+1, j+1, ' ', format)
            worksheet.set_row(k, 70)

        else:
            info = u"FRENTE/ %s_%s AT'N: %s %s (%s) RUTA %s_%s DIR: %s %s %s %s DOT: %s %s" % (clientes[i].subcategoria3,
                                                                              clientes[i].empresa,
                                                                              clientes[i].nombre,
                                                                              clientes[i].apellido_Paterno,
                                                                              clientes[i].puesto,
                                                                              nr,
                                                                              clientes[i].ordenentrega,
                                                                              clientes[i].calle,
                                                                              clientes[i].numero_Exterior,
                                                                              clientes[i].numero_Interior,
                                                                              clientes[i].referencia,
                                                                              clientes[i].adicional,
                                                                              clientes[i].day)
            worksheet.write(k, j*2, info, format)
            worksheet.write(k+1, j+1, ' ', format)
            worksheet.set_row(k, 70)
            j += 1

    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=etiquetas.xlsx"

    return response