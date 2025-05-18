from django.db import models
from django.core.validators import EmailValidator

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=100,
        unique=True,
        validators=[EmailValidator(message="Email inválido")]
    )
    telefono = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'clientes'  # Buena práctica: nombres explícitos

    def __str__(self):
        return f"{self.nombre} ({self.email})"