from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

# ------------ EVENTO ------------

class Evento(models.Model):

    titulo = models.CharField(max_length=200, verbose_name="Título del Evento") 
    fecha_hora = models.DateTimeField(verbose_name="Fecha y Hora") 
    lugar = models.CharField(max_length=255, verbose_name="Lugar") 
    
    imagen = models.ImageField(upload_to='event_images/', null=True, blank=True, verbose_name="Imagen")
    
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor de Entrada")
    plazas_totales = models.IntegerField(default=0, verbose_name="Plazas Totales") 
    plazas_disponibles = models.IntegerField(default=0, verbose_name="Plazas Disponibles") 

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['fecha_hora']

    def __str__(self):
        return f"{self.titulo} ({self.fecha_hora.strftime('%Y-%m-%d %H:%M')})"

    def save(self, *args, **kwargs):

        if not self.pk: 
            self.plazas_disponibles = self.plazas_totales
        super().save(*args, **kwargs)

# ------------ INSCRIPCION ------------

class Inscripcion(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario Registrado")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inscripción")

    class Meta:
        unique_together = ('usuario', 'evento')
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"Inscripción de {self.usuario.username} a {self.evento.titulo}"
    
    def clean(self):

        if self.pk is None and self.evento.plazas_disponibles <= 0:
            raise ValidationError('No quedan plazas disponibles para este evento.')

@receiver(post_save, sender=Inscripcion)
def disminuir_plazas(sender, instance, created, **kwargs):

    if created:
        evento = instance.evento
        if evento.plazas_disponibles > 0:
            evento.plazas_disponibles -= 1
            evento.save(update_fields=['plazas_disponibles'])
        
@receiver(post_delete, sender=Inscripcion)
def aumentar_plazas(sender, instance, **kwargs):

    evento = instance.evento
    evento.plazas_disponibles += 1
    evento.save(update_fields=['plazas_disponibles'])