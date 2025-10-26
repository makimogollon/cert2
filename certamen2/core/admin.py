from django.contrib import admin
from .models import Evento, Inscripcion

# Register your models here.

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_hora', 'lugar', 'plazas_totales', 'plazas_disponibles', 'valor')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('evento', 'usuario', 'fecha_inscripcion')