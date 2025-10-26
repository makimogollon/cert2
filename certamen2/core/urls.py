from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),    
    path('eventos/', views.eventos, name='eventos'), 
    path('comunidad/', views.comunidad, name='comunidad'),

    # eventos
    path('', views.lista_eventos, name='lista_eventos'),
    path('registro/', views.registro_usuario, name='registro_usuario'), 

    # usuarios autenticados
    path('evento/<int:evento_id>/inscribirse/', views.inscribirse, name='inscribirse'), 
    path('mis_eventos/', views.mis_eventos, name='mis_eventos'), 
    path('inscripcion/<int:inscripcion_id>/anular/', views.anular_inscripcion, name='anular_inscripcion'),

]
