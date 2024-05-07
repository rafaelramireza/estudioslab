from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Turno, TipoEstudio
from .models import Paciente
from django.db import connection
from django.utils import timezone
from django.db.models import Count



from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Turno, TipoEstudio, Paciente
from django.utils import timezone

def emitir_turno(request):
    if request.method == 'POST':
        # Procesar los datos del formulario
        tipo_estudio_id = request.POST.get('tipo_estudio')
        nombre_paciente = request.POST.get('nombre_paciente')
        apellido_paciente = request.POST.get('apellido_paciente')
        identificacion_paciente = request.POST.get('identificacion')
        contacto_paciente = request.POST.get('contacto')
        estado = request.POST.get('estado')

        # Obtener el último turno creado
        ultimo_turno = Turno.objects.order_by('-numero_turno').first()

        # Calcular el número de turno para el nuevo paciente
        if ultimo_turno:
            nuevo_numero_turno = ultimo_turno.numero_turno + 1
        else:
            nuevo_numero_turno = 1  # Si no hay turnos previos, empezamos desde 1

        # Crear y guardar el paciente en la base de datos
        paciente = Paciente.objects.create(
            nombre=nombre_paciente,
            apellido=apellido_paciente,
            identificacion=identificacion_paciente,
            contacto=contacto_paciente
        )

        # Obtener el tipo de estudio
        tipo_estudio = TipoEstudio.objects.get(pk=tipo_estudio_id)

        # Crear y guardar el nuevo turno en la base de datos
        Turno.objects.create(
            numero_turno=nuevo_numero_turno,
            tipo_estudio=tipo_estudio,
            paciente=paciente,
            fecha_hora_emision=timezone.now(),
            estado=estado
        )

        # Redireccionar a la página de confirmación de turno
        return redirect('confirmacion_turno')

    tipos_estudio = TipoEstudio.objects.all()
    return render(request, 'emitir_turno.html', {'tipos_estudio': tipos_estudio})



def confirmacion_turno(request):
    # Obtener el último turno creado
    ultimo_turno = Turno.objects.latest('id')

    return render(request, 'confirmacion_turno.html', {'ultimo_turno': ultimo_turno})

def generar_reporte(request):
    turnos_emitidos = []
    estudios_totales = []

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        fecha_inicio = timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = timezone.datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        turnos_emitidos = Turno.objects.filter(fecha_hora_emision__date__range=(fecha_inicio, fecha_fin))

        estudios_totales = Turno.objects.filter(fecha_hora_emision__date__range=(fecha_inicio, fecha_fin)) \
                                         .values('tipo_estudio__nombre') \
                                         .annotate(total=Count('tipo_estudio__nombre'))

    return render(request, 'emitir_reporte.html', {'turnos_emitidos': turnos_emitidos, 'estudios_totales': estudios_totales})