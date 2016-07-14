# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import *
from django.conf import settings
import random

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

class LoginForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Usuario'
		self.fields['password'].label = 'Contraseña'
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
	password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Contraseña'}))

class CreateCliente(ModelForm):

	class Meta:
		model = Cliente
		fields = ('nombre','apellido_Paterno','apellido_Materno','puesto','telefono','mail')

class CreateRuta(ModelForm):

	class Meta:
		model = Ruta
		fields = '__all__'

class CreateRepartidor(ModelForm):

	class Meta:
		model = Repartidor
		fields = '__all__'

class CreateCupon(forms.ModelForm):
	cupon =  forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
	fechafinal = forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
	def __init__(self, *args, **kwargs):
		super(CreateCupon, self).__init__(*args, **kwargs)
		self.fields['campania'].label = 'Nombre de la Campaña'
		self.fields['membresia'].label = 'Tipo de Membresia'
		self.fields['cantidad'].label = 'Cupones Permitidos'

	class Meta:
		model = Cupon
		fields = ('campania','membresia','cupon','fechafinal','cantidad')
		widgets = {
            'membresia': forms.RadioSelect(),
        }

class UpdateCupon(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UpdateCupon, self).__init__(*args, **kwargs)
		self.fields['campania'].label = 'Nombre de la Campaña'
		self.fields['cantidad'].label = 'Cupones Permitidos'

	class Meta:
		model = Cupon
		fields = ('campania','cupon','cantidad','activo')
		widgets = {
            'membresia': forms.RadioSelect(),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateClienteFrente(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CreateClienteFrente, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = 'Nombre*'
		self.fields['apellido_Paterno'].label = 'Apellido Paterno*'
		self.fields['cumpleanos'].label = 'Cumpleaños'
		self.fields['mail'].label = 'Correo Electrónico*'
		self.fields['numero_Exterior'].label = 'Número Exterior*'
		self.fields['numero_Interior'].label = 'Número Interior'
		self.fields['cp'].label = 'Código Postal*'
		self.fields['delegacion'].label = 'Delegación*'
		self.fields['entregas'].label = 'Lugar de Entrega*'
		self.fields['cupon'].label = 'Cupón*'
		self.fields['phone'].label = 'Teléfono*'
		self.fields['Colonia'].label = 'Colonia**'
		self.fields['calle'].label = 'Calle*'

	class Meta:
		model = ClienteFrente
		fields = ('nombre','apellido_Paterno','apellido_Materno', 'cumpleanos', 'mail','phone','calle','numero_Exterior','numero_Interior', 'cp','delegacion','Colonia','referencia','entregas','empresa','puesto','cupon')
		widgets = { 'empresa': forms.HiddenInput()}

class CreateClienteCupon(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CreateClienteCupon, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = 'Nombre*'
		self.fields['apellido_Paterno'].label = 'Apellido Paterno*'
		self.fields['cumpleanos'].label = 'Cumpleaños'
		self.fields['mail'].label = 'Correo Electrónico*'
		self.fields['numero_Exterior'].label = 'Número Exterior*'
		self.fields['numero_Interior'].label = 'Número Interior'
		self.fields['cp'].label = 'Código Postal*'
		self.fields['delegacion'].label = 'Delegación*'
		self.fields['entregas'].label = 'Lugar de Entrega*'
		self.fields['phone'].label = 'Teléfono*'
		self.fields['Colonia'].label = 'Colonia**'
		self.fields['calle'].label = 'Calle*'

	class Meta:
		model = ClienteFrente
		fields = ('nombre','apellido_Paterno','apellido_Materno', 'cumpleanos', 'mail','phone','calle','numero_Exterior','numero_Interior', 'cp','delegacion','Colonia','referencia','entregas','empresa','puesto','cupon')
		widgets = { 'cupon': forms.HiddenInput(), 'empresa': forms.HiddenInput()}
		

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ('nombreEmpresa',) 
    

class updateUser(ModelForm):

	class Meta:
		model = ClienteFrente
		fields = ('cupon',)


class updateUserPR(ModelForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username')