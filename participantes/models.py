import uuid
from django.db import models

class Participante(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    password = models.CharField(max_length=128, blank=True)  # Almacenada encriptada
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
