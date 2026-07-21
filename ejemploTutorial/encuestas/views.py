from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *

# Pagina de inicio, lista encuestas
def home_view(request):
    preguntas = Pregunta.objects.all()

    context = {
        'preguntas' : preguntas
    }

    return render(request, 'index.html', context)

# Mostrar resultados encuesta
def resultados_view(request, pregunta_id):
    pregunta = Pregunta.objects.get(pk=pregunta_id)

    total_votos = 0
    for opcion in pregunta.opcion_set.all():
        total_votos += opcion.votos

    context = {
        "pregunta": pregunta,
        "total_votos": total_votos
    }

    return render(request, 'resultados.html', context)

# Votar encuesta
def votar_view(request, pregunta_id):
    pregunta = Pregunta.objects.get(id=pregunta_id)

    if request.method == "POST":
        opcion_id = request.POST.get("opcion")

        if not opcion_id:
            return render(request, "votar.html", {
                "pregunta": pregunta,
                "error": "Debes seleccionar una opción."
            })

        opcion = Opcion.objects.get(id=opcion_id)
        opcion.votos += 1
        opcion.save()

        return redirect("resultados", pregunta_id=pregunta.id)

    return render(request, "votar.html", {
        "pregunta": pregunta
    })


# Sistema de login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "username": username,
                "error": "Usuario o contraseña incorrectos."
            })

    return render(request, "login.html")

# Sistema de logout
def logout_view(request):
    logout(request)
    return redirect("home")

# Crear encuesta
@login_required
def crear_view(request):
    if request.method == "POST":
        pregunta_form = PreguntaForm(request.POST)
        opciones_formset = OpcionFormSet(request.POST)

        if pregunta_form.is_valid() and opciones_formset.is_valid():
            pregunta = pregunta_form.save()
            opciones_formset.instance = pregunta
            opciones_formset.save()

            return redirect('home')
    else:
        pregunta_form = PreguntaForm()
        opciones_formset = OpcionFormSet()

    return render(request, "crear.html", {
        "pregunta_form": pregunta_form,
        "opciones_formset": opciones_formset,
    })

# Editar encuesta
@login_required
def editar_view(request, pregunta_id):
    pregunta = Pregunta.objects.get(id=pregunta_id)

    if request.method == "POST":
        pregunta_form = PreguntaForm(
            request.POST,
            instance=pregunta
        )

        opciones_formset = OpcionFormSet(
            request.POST,
            instance=pregunta
        )

        if pregunta_form.is_valid() and opciones_formset.is_valid():
            pregunta_form.save()
            opciones_formset.save()

            return redirect("home")

    else:
        pregunta_form = PreguntaForm(
            instance=pregunta
        )

        opciones_formset = OpcionFormSet(
            instance=pregunta
        )

    return render(request, "crear.html", {
        "pregunta_form": pregunta_form,
        "opciones_formset": opciones_formset,
    })

# Eliminar encuesta
@login_required
def eliminar_view(request, pregunta_id):
    pregunta = Pregunta.objects.get(id=pregunta_id)

    if request.method == "POST":
        pregunta.delete()
        return redirect("home")

    return render(request, "eliminar.html", {
        "pregunta": pregunta
    })


