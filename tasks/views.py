from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # UserCreationForm me devuelve un formulario para crear un usuario, AuthenticationForm es para iniciar sesion con un usuario ya guardado
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate #el login crea la cookie para autenticar el usuario, el authenticated me irve para saber si el usuario se guardo o esta autenticado en la base de datos
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required #esto es para proteger las rutas

# Create your views here.

# def helloworld(request):
#     title = "Hello World"
#     return render(request, 'signup.html', {
#         "form": UserCreationForm
#     })
    
def home(request):
    title = "Hello World"
    return render(request, 'tasks/home.html')



def signup(request): #registro de usuarios
    
    if request.method == "GET": #mostrar informacion en pantalla
        # print("enviando formulario")
        return render(request, 'tasks/signup.html', {
        "form": UserCreationForm
    })
    else:
        if request.POST["password1"] == request.POST["password2"]:  #con el post se recibe los datos del formulario y se procede a crear al usuario en la DB
            #register user
            try:
                user=User.objects.create_user(username=request.POST["username"], password=request.POST["password1"]) #se crea el usuario en la base de datos en la tabla user
                user.save()
                # return HttpResponse("User created succesfully")
                login(request, user) #el login crea la cookie para autenticar el usuario
                return redirect('hello_app:tasks') #hay que colocarle el nombre de la app de las urls para que pueda redireccionar
            
            except IntegrityError:
                return render(request, 'tasks/signup.html', { #si el usuario ya existe te quedas en ese mismo render con la misma ruta pero le envias el error de que ya existe el usuario
                    "form": UserCreationForm,
                    "error": "Username already exists"
                })
           
        return render(request, 'tasks/signup.html', {
                    "form": UserCreationForm,
                    "error": "password do no match"
                })
            
            
            
        # print(request.POST) #se ven los datos que el cliente envia
        # print("obteniendo datos")
        

@login_required #este decorador es para proteger las rutas
def tasks(request):
    print(request)
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) #vas a traer las que estan vacias, sirve para mostrar al usuario los que le faltan hacer
    return render(request, "tasks/tasks.html", {"tasks": tasks, "task_pending":True})

def signout(request): #esto cierra la sesion
    logout(request)
    return redirect("hello_app:home")

def signin(request):
    if request.method == "GET": #si e get quiere decir que va a renderizar, no va a mandar la informacion
         return render(request, "tasks/signin.html", {
            "form": AuthenticationForm   #esto añade el formulario para iniciar sesion que ya te permite autenticar
        })
    else: #aqui es POST por ende se envia los datos
        user=authenticate(request, username=request.POST["username"], password=request.POST["password"]) #va a verificar si el usuario esta en la DB
        if user is None: #si no encuentra el usuario en la base de datos entonces mandas un error y renderizas signin.html
            return render(request, "tasks/signin.html", {
                "form": AuthenticationForm,
                'error': "Username or password is incorrect"
            })
        else: #si si encontro el usuario 
            login(request, user) #guarda la sesion iniciada
            return redirect("hello_app:tasks")
        
#CRUD

#CREATE 

@login_required
def create_task(request):
    
    if request.method == "GET":
        return render(request, "tasks/create_task.html", {
        "form": TaskForm
    })
    else: 
        try:
            form=TaskForm(request.POST)
            new_task = form.save(commit=False) #esto es para que no me guarde los datos si no que lo envie y los muestra
            new_task.user = request.user #trae al usuario de la tarea que eta registrado
            new_task.save() #aqui si guarda el formulario
            print(form) #trae la informacion enviada en el formulario
            return redirect("hello_app:tasks")
        except ValueError:
               return render(request, "tasks/create_task.html", {
                "form": TaskForm,
                "error": "Please provide valid data"
                        })
#READ (GET) y UPDATE

@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        print(task_id)
        task=get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task) #me llena el formulario con los datos del task, esto es para poder actualizar
        return render(request, "tasks/task_detail.html", {"task": task, "form": form})
    else:
        try:
            print(request.POST) #me trae la informacion que colocamos en el formulario
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task) #aqui guardamos la nueva informacion que colocamos en el formulario
            form.save()
            return redirect("hello_app:tasks")
        except ValueError:
              return render(request, "tasks/task_detail.html", {"task": task, "form": form, "error":"Error updating task"})
          
#COMPLETED

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now() #cambia la fecha a la fecha completada
        task.save()
        return redirect("hello_app:tasks")
    
#DELETE

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("hello_app:tasks")
    
#listar tarea completadas

@login_required
def tasks_completed(request):
    print(request)
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #vas a traer las tareas que tienen una fecha completada y ordenarla
    return render(request, "tasks/tasks.html", {"tasks": tasks})

    
    
            
            
                
            
    
            
            
       
   
    
   
    