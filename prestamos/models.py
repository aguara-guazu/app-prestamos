from datetime import datetime
from uuid import uuid4

from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    genero = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino'), ('X', 'No binario')))
    dni = models.BigIntegerField(blank=False, null=False)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_solicitud = models.DateField(default=datetime.today)
    estado = models.CharField(max_length=1, choices=(('A', 'Aprobado'), ('R', 'Rechazado')))
    transacion_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.cliente, self.fecha_solicitud, self.monto, self.estado, self.transacion_id)
