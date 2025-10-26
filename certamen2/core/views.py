from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db import IntegrityError
from .models import Evento, Inscripcion

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def eventos(request):
    return render(request, 'core/eventos.html')

def comunidad(request):
    return render(request, 'core/comunidad.html')

# ---------- 3. INFO DE EVENTOS ----------

def lista_eventos(request):

    eventos = Evento.objects.all()
    data = {
        'eventos': eventos
    }
    return render(request, 'core/lista_eventos.html', data)

# ---------- 4. CREAR CUENTA USUARIO ----------

def registro_usuario(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Cuenta creada con éxito para {user.username}. ¡Ya puedes iniciar sesión!')
            return redirect('lista_eventos')
    else:
        form = UserCreationForm()

    data = {
        'form': form
    }

    return render(request, 'core/registro.html', data)


#---------- 6. INSCRIBIRSE A LOS EVENTOS ----------

@login_required 
def inscribirse(request, evento_id):

    evento = get_object_or_404(Evento, pk=evento_id)

    if Inscripcion.objects.filter(usuario=request.user, evento=evento).exists():
        messages.warning(request, f'Ya estás inscrito(a) en el evento: {evento.titulo}.')
        return redirect('mis_eventos')

    if evento.plazas_disponibles <= 0:
        messages.error(request, f'Lo sentimos, no quedan plazas disponibles para {evento.titulo}.')
        return redirect('lista_eventos')

    try:
        Inscripcion.objects.create(usuario=request.user, evento=evento)

        messages.success(request, f'¡Inscripción exitosa! Te has registrado en: {evento.titulo}.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al intentar inscribirte: {e}')

    return redirect('mis_eventos') 

#--------- 7. VER EVENTOS INSCRITOS ----------

@login_required
def mis_eventos(request):

    inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('evento')
    
    data = {
        'inscripciones': inscripciones
    }

    return render(request, 'core/mis_eventos.html', data)

#--------- 7. ANULAR INSCRIPCIÓN A EVENTOS ----------

@login_required
def anular_inscripcion(request, inscripcion_id):

    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)

    if inscripcion.usuario != request.user:
        messages.error(request, 'No tienes permiso para anular esta inscripción.')
        return redirect('mis_eventos') 

    evento_titulo = inscripcion.evento.titulo
    inscripcion.delete() 

    messages.success(request, f'Has anulado tu registro en el evento: {evento_titulo}.')
    return redirect('mis_eventos')