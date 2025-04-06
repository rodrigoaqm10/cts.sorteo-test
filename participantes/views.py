from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.conf import settings
import random

from .models import Participante
from .serializers import ParticipanteSerializer

# Vista unificada: registra al participante y envía el correo de verificación
class RegistroCompletoView(APIView):
    def post(self, request):
        nombre = request.data.get("nombre")
        email = request.data.get("email")
        telefono = request.data.get("telefono")

        # Validar que se reciban todos los datos necesarios
        if not nombre or not email or not telefono:
            return Response({"error": "Datos incompletos."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el email ya existe
        if Participante.objects.filter(email=email).exists():
            return Response({"error": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el participante
        participante = Participante.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono
        )

        # Construir la URL de verificación: primero pasa por el endpoint /verificar/
        verification_url = f"http://localhost:8000/api/participantes/verificar/{participante.verification_token}/"

        # Redactar un correo elegante para la verificación
        subject = "Activa tu cuenta para el sorteo de San Valentín"
        message = (
            f"Estimado/a {nombre},\n\n"
            "¡Gracias por registrarte en nuestro sorteo para ganar una estadía romántica de 2 noches con todo pagado! "
            "Para completar tu registro y activar tu cuenta, por favor haz clic en el siguiente enlace:\n\n"
            f"{verification_url}\n\n"
            "Si no solicitaste este registro, ignora este mensaje.\n\n"
            "Saludos cordiales,\n"
            "Equipo del Hotel"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response(
            {"mensaje": "Registro exitoso, se ha enviado el correo de verificación."},
            status=status.HTTP_201_CREATED
        )

# Vista para crear participante (opcional)
class ParticipanteCreateView(generics.CreateAPIView):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        if Participante.objects.filter(email=email).exists():
            return Response({"error": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

# Enviar correo de verificación (opcional)
class EnviarCorreoVerificacion(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            participante = Participante.objects.get(email=email)
            verification_url = f"http://localhost:8000/api/participantes/verificar/{participante.verification_token}/"
            subject = "Activa tu cuenta para el sorteo de San Valentín"
            message = (
                f"Estimado/a {participante.nombre},\n\n"
                "Para activar tu cuenta y participar en nuestro sorteo, haz clic en el siguiente enlace:\n\n"
                f"{verification_url}\n\n"
                "Si no solicitaste este registro, por favor ignora este mensaje.\n\n"
                "Atentamente,\n"
                "Equipo del Hotel"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({"mensaje": "Correo enviado"}, status=status.HTTP_200_OK)
        except Participante.DoesNotExist:
            return Response({"error": "Participante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Endpoint para verificar el email: marca al participante como verificado y redirige al frontend para crear contraseña
class VerificarParticipante(APIView):
    def get(self, request, token):
        try:
            participante = Participante.objects.get(verification_token=token)
            participante.verificado = True
            participante.save()
            return redirect(f"http://localhost:8080/#/crear-contrasena/{participante.verification_token}")
        except Participante.DoesNotExist:
            return render(request, 'correo_invalido.html')

# Crear contraseña
class CrearContrasenaView(APIView):
    def post(self, request, token):
        password = request.data.get("password")
        if not password:
            return Response({"error": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            participante = Participante.objects.get(verification_token=token)
            participante.password = make_password(password)
            participante.save()
            return Response({"mensaje": "Contraseña creada correctamente"})
        except Participante.DoesNotExist:
            return Response({"error": "Token inválido"}, status=status.HTTP_404_NOT_FOUND)

# Generar ganador y notificar
class GenerarGanador(APIView):
    def post(self, request):
        participantes_verificados = Participante.objects.filter(verificado=True)
        if not participantes_verificados.exists():
            return Response({"error": "No hay participantes verificados."}, status=status.HTTP_400_BAD_REQUEST)
        ganador = random.choice(list(participantes_verificados))
        subject = "¡Felicidades! Eres el ganador de nuestra promoción de San Valentín"
        message = (
            f"Estimado/a {ganador.nombre},\n\n"
            "Nos complace informarte que has sido seleccionado como ganador de nuestro sorteo para una estadía de 2 noches con todo pagado. "
            "Nos pondremos en contacto contigo para coordinar los detalles de tu premio.\n\n"
            "¡Felicidades y disfruta de esta experiencia única!\n\n"
            "Atentamente,\n"
            "Equipo del Hotel"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [ganador.email],
            fail_silently=False,
        )
        return Response({"mensaje": f"El ganador es {ganador.nombre} ({ganador.email})"}, status=status.HTTP_200_OK)

# Vista para eliminar un participante verificado
class DeleteParticipanteView(APIView):
    def delete(self, request, pk):
        try:
            participante = Participante.objects.get(id=pk)
            participante.delete()
            return Response({"mensaje": "Participante eliminado."}, status=status.HTTP_200_OK)
        except Participante.DoesNotExist:
            return Response({"error": "Participante no encontrado."}, status=status.HTTP_404_NOT_FOUND)

# Vista para listar participantes verificados
from rest_framework.generics import ListAPIView
class VerificadosList(ListAPIView):
    queryset = Participante.objects.filter(verificado=True)
    serializer_class = ParticipanteSerializer
