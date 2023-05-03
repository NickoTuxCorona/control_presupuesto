from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def crear_usuario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Crear el usuario
        user = User.objects.create_user(username=username, email=email, password=password)

        # Guardar el usuario en la base de datos
        user.save()

        # Redirigir a una página de éxito
        return HttpResponseRedirect('/exito/')
    else:
        # Mostrar el formulario
        return render(request, 'crear_usuario.html')