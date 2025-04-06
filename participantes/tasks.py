from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def enviar_correo_verificacion(email, token, nombre, verification_url):
    subject = 'Verifica tu cuenta para el sorteo del Hotel'
    message = f'Hola {nombre},\n\nPara activar tu registro, haz clic en el siguiente enlace:\n{verification_url}\n\n¡Suerte!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task
def enviar_correo_ganador(email, nombre):
    subject = '¡Felicidades! Has ganado la estadía'
    message = f'Hola {nombre},\n\n¡Enhorabuena! Has sido seleccionado como ganador del sorteo para una estadía de 2 noches con todo pagado. Nos estaremos contactando contigo.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
