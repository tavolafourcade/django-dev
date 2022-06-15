from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CursosFormulario(forms.Form):
  #Especificar los campos
  curso = forms.CharField(max_length=50)
  camada = forms.IntegerField()

class ProfesorFormulario(forms.Form):
  nombre = forms.CharField(max_length=30)
  apellido = forms.CharField(max_length=30)
  email = forms.EmailField()
  profesion = forms.CharField(max_length=30)
 
class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True)
  password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
  password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
  class Meta: #Esto es para que el formulario sepa que campos tiene que mostrar
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    help_texts={k:"" for k in fields} #Esto es para que el formulario no muestre los mensajes de ayuda

class UserEditForm(UserCreationForm):
  email = forms.EmailField(required=True)
  password1 = forms.CharField(label="Modificar Contraseña", widget=forms.PasswordInput)
  password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

  last_name = forms.CharField(label="Modificar Apellido")
  first_name = forms.CharField(label="Modificar Nombre")

  class Meta: #Esto es para que el formulario sepa que campos tiene que mostrar
    model = User
    fields = ['email', 'password1', 'password2', 'last_name', 'first_name']
    help_texts={k:"" for k in fields} #Esto es para que el formulario no muestre los mensajes de ayuda