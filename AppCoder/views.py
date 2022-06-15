from django.http import HttpResponse
from django.shortcuts import render
from AppCoder.models import Curso, Profesor, Estudiante, Avatar
from django.template import loader
from AppCoder.forms import CursosFormulario, ProfesorFormulario, UserRegistrationForm, UserEditForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

def curso(self):
  curso = Curso(nombre="Desarrollo backend", camada=18340)
  curso.save()
  documento = f"Curso: {curso.nombre} - Camada: {curso.camada}"
  return HttpResponse(documento)

def profesores(request):
  return render(request, 'AppCoder/profesores.html')

def cursos(request):
  return render(request, 'AppCoder/cursos.html')

def estudiantes(request):
  return render(request, 'AppCoder/estudiantes.html')

def entregables(request):
  return render(request, 'AppCoder/entregables.html')

def cursosFormulario(request):
  if request.method == 'POST':
    miFormulario = CursosFormulario(request.POST)
    
    if miFormulario.is_valid():
      informacion = miFormulario.cleaned_data # Esto me trae los datos limpios
      curso = Curso(nombre=informacion['curso'], camada=informacion['camada'])
      curso.save()
      return render(request, 'AppCoder/inicio.html')
    
  else:
    miFormulario = CursosFormulario() #Creo mi formulario vacío
  return render(request, 'AppCoder/cursosFormulario.html', {'miFormulario':miFormulario})

@login_required
def inicio(request):
  avatars = Avatar.objects.filter(user=request.user.id)
  return render(request, 'appCoder/inicio.html', {'url': avatars[0].avatar.url})
  # plantilla = loader.get_template('AppCoder/inicio.html')
  # documento = plantilla.render()
  # return HttpResponse(documento)

def profesorFormulario(request):
  if request.method == 'POST':
    miFormulario = ProfesorFormulario(request.POST)
    if miFormulario.is_valid():
      informacion = miFormulario.cleaned_data
    nombre = informacion['nombre']
    apellido = informacion['apellido']
    email = informacion['email']
    profesion = informacion['profesion']

    profesor = Profesor(nombre=nombre, apellido=apellido, email=email, profesion=profesion)
    profesor.save()
    return render(request, 'AppCoder/inicio.html')
  else:
    miFormulario = ProfesorFormulario()
  return render(request, 'appCoder/profesorFormulario.html', {'miFormulario':miFormulario})

def busquedaComision(request):
  return render(request, 'AppCoder/busquedaComision.html')

def buscar(request):
  if request.GET['camada']:
    camada = request.GET['camada']
    # Del modelo Curso filtrame los cursos que tengan como camada la variable camada
    cursos = Curso.objects.filter(camada=camada)
    # Quiero que me renderice cursos y a la vez me mande la lista de los cursos como contexto
    return render(request, 'AppCoder/resultadosBusqueda.html', {'cursos':cursos, 'camada':camada})
  else:
    respuesta = "No se ingresó ninguna comisión"
    return HttpResponse(respuesta)

def leerProfesores(request):
  profesores = Profesor.objects.all() # Traigo todos los profesores de la base de datos
  contexto = {'profesores':profesores}
  return render(request, 'AppCoder/profesores.html', contexto)

@login_required
def eliminarProfesor(request, nombre):
  profesor = Profesor.objects.get(nombre=nombre)
  profesor.delete()

  profesores = Profesor.objects.all()
  contexto = {'profesores':profesores}
  return render(request, 'AppCoder/profesores.html', contexto)

def editarProfesor(request, nombre):
  profesor = Profesor.objects.get(nombre=nombre) # Obtengo el profesor a modificar
  if request.method == 'POST':
    miFormulario = ProfesorFormulario(request.POST) # Creo mi formulario con los datos del profesor
    if miFormulario.is_valid():
      informacion = miFormulario.cleaned_data # Esto me trae los datos limpios
      profesor.nombre = informacion['nombre']
      profesor.apellido = informacion['apellido']
      profesor.email = informacion['email']
      profesor.profesion = informacion['profesion']
      profesor.save()
      # Luego muestro la vista de profesores nuevamente
      profesores = Profesor.objects.all()
    contexto = {'profesores':profesores}
    return render(request, 'AppCoder/profesores.html', contexto)
  else: # Si no es POST, entonces es GET
    miFormulario = ProfesorFormulario(initial={'nombre':profesor.nombre, 'apellido':profesor.apellido, 'email':profesor.email, 'profesion':profesor.profesion})
    contexto = {'miFormulario':miFormulario, 'nombre':nombre}
    return render(request, 'AppCoder/editarProfesor.html', contexto)

#------------------------------------------------------------------------------------------------------------------

class EstudiantesList(LoginRequiredMixin, ListView):
  model = Estudiante
  template_name = 'AppCoder/estudiante_list.html'

class EstudianteDetalle(DetailView):
  model = Estudiante
  template_name = 'AppCoder/estudiante_detalle.html'

class EstudianteCreacion(CreateView):
  model = Estudiante
  success_url = reverse_lazy('estudiante_listar') # Redirecciono a la vista de estudiantes luego de crear un estudiante
  fields = ['nombre', 'apellido', 'email']

class EstudianteEdicion(UpdateView):
  model = Estudiante
  success_url = reverse_lazy('estudiante_listar')
  fields = ['nombre', 'apellido', 'email']

class EstudianteEliminacion(DeleteView):
  model = Estudiante
  success_url = reverse_lazy('estudiante_listar')

#------------------------------------------------------------------------------------------------------------------

def login_request(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      usuario = form.cleaned_data.get('username')
      clave = form.cleaned_data.get('password')
      # Autenticación de usuario
      user = authenticate(username=usuario, password=clave) # Si este usuario existe me lo trae
      if user is not None:
        login(request,user) # Si existe, lo loguea
        return render(request, 'AppCoder/inicio.html', {'mensaje': f'Bienvenido {usuario}'})
      else:
        return render(request, 'AppCoder/inicio.html', {'mensaje': 'Error, datos incorrectos'})
    else:
      return render(request,'AppCoder/inicio.html', {'mensaje': 'Error, formulario erróneo'})
  
  form = AuthenticationForm() # Creo un formulario vacío si vengo por GET
  return render(request, 'AppCoder/login.html', {'form':form})

def registro(request):
  if request.method == 'POST': # Si es POST, entonces es un formulario que viene lleno
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      form.save()
      return render(request, 'AppCoder/inicio.html', {'mensaje': f'Usuario {username} creado correctamente'})
    else:
      return render(request, 'AppCoder/inicio.html', {'mensaje': 'Error, no se pudo crear el usuario'})
  else:
    form = UserRegistrationForm()
    return render(request, 'AppCoder/registro.html', {'form': form})

@login_required
def editarPerfil(request):
  usuario = request.user

  if request.method == 'POST':
    formulario = UserEditForm(request.POST, instance=usuario)
    if formulario.is_valid():
      informacion = formulario.cleaned_data
      usuario.email = informacion['email']
      usuario.password1 = informacion['password1']
      usuario.password2 = informacion['password2']
      usuario.save()

      return render(request, 'AppCoder/inicio.html', {'usuario': usuario, 'mensaje': 'Datos actualizados correctamente'})
  else:
    formulario = UserEditForm(instance=usuario)
  return render(request, 'AppCoder/editarPerfil.html', {'formulario': formulario, 'usuario': usuario.username})