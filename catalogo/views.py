from django.shortcuts import render
from .models import ProgramaAcademico, Universidad



# Create your views here.
def lista_programas(request):

    busqueda = request.GET.get('busqueda') if request.GET.get('busqueda') else ''
    especialidad_id = request.GET.get('especialidad_id')
    especialidad_id = int(especialidad_id) if especialidad_id else ''
    id_universidad = request.GET.get('id_universidad')
    id_universidad = int(id_universidad) if id_universidad else ''

    programas_academicos = ProgramaAcademico.objects

    if busqueda:
        programas_academicos = programas_academicos.filter(
            nombre_programa__unaccent__icontains=busqueda
        )

    if id_universidad:
        programas_academicos = programas_academicos.filter(
            id_universidad=id_universidad
        )

    programas_academicos = programas_academicos.all()

    universidades = Universidad.objects.all()

    return render(request, 'lista_programas.html',
                  {'programas_academicos': programas_academicos,
                   'busqueda': busqueda,
                   'id_universidad': id_universidad,
                   'universidades': universidades})