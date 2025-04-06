from django.urls import path
from .views import (
    RegistroCompletoView,
    ParticipanteCreateView,
    EnviarCorreoVerificacion,
    VerificarParticipante,
    CrearContrasenaView,
    GenerarGanador,
    VerificadosList,
    DeleteParticipanteView
)

urlpatterns = [
    # Endpoint unificado para registro y envío de correo
    path('registro-completo/', RegistroCompletoView.as_view(), name='registro_completo'),
    # Rutas adicionales (opcional)
    path('', ParticipanteCreateView.as_view(), name='crear_participante'),
    path('enviar-correo/', EnviarCorreoVerificacion.as_view(), name='enviar_correo'),
    path('verificar/<uuid:token>/', VerificarParticipante.as_view(), name='verificar_participante'),
    path('crear-contrasena/<uuid:token>/', CrearContrasenaView.as_view(), name='crear_contrasena'),
    path('generar-ganador/', GenerarGanador.as_view(), name='generar_ganador'),
    # Nuevo endpoint para listar participantes verificados
    path('verificados/', VerificadosList.as_view(), name='verificados'),
     # Nuevo endpoint para eliminar un participante, se espera el id (entero)
    path('eliminar/<int:pk>/', DeleteParticipanteView.as_view(), name='eliminar_participante'),
]
