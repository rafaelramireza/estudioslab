from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    identificacion = models.PositiveSmallIntegerField()
    contacto = models.CharField(max_length=100)

    class Meta:
        db_table = 'Pacientes'

class TipoEstudio(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'TiposEstudio'
        
class Turno(models.Model):
    numero_turno = models.IntegerField()
    tipo_estudio = models.ForeignKey(TipoEstudio, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=25, choices=[('paciente nuevo', 'Paciente Nuevo'), ('paciente con expediente', 'Paciente con Expediente')])

    class Meta:
        db_table = 'Turnos'
