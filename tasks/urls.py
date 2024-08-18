from django.urls import path
from .views import home, signup, tasks, signout, signin, create_task, task_detail, complete_task, delete_task, tasks_completed
app_name='hello_app'



urlpatterns = [
    path('', home, name="home"),
    path('signup/', signup, name="signup"), #esta ruta signup/ es la que se envia en el action del formulario y se recibe en el request
    path('tasks/', tasks, name="tasks"),
    path('logout/', signout, name="logout"),
    path('signin/', signin, name="signin"),
    path('create/task/', create_task, name="create_tasks"),
    path("tasks/<int:task_id>", task_detail, name="task_detail"), #con <> le pasamos un parametro al metodo task_detail en este caso el id
    path("tasks/<int:task_id>/complete", complete_task, name="complete_task"), #esto es para marcar las tareas completadas
    path("tasks/<int:task_id>/delete", delete_task, name="delete_task"), #esto es  para eliminar las tareas
    path("tasks_completed", tasks_completed, name="tasks_completed"), #eto es para realizar una lista de tareas completadas
    
]