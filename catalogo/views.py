from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import ProgramaAcademico, Universidad, Admision


# Create your views here.
def lista_programas(request):

    busqueda = request.GET.get("busqueda") if request.GET.get("busqueda") else ""
    especialidad_id = request.GET.get("especialidad_id")
    especialidad_id = int(especialidad_id) if especialidad_id else ""
    id_universidad = request.GET.get("id_universidad")
    id_universidad = int(id_universidad) if id_universidad else ""

    programas_academicos = ProgramaAcademico.objects

    if busqueda:
        programas_academicos = programas_academicos.filter(
            nombre_programa__unaccent__icontains=busqueda
        )

    if id_universidad:
        programas_academicos = programas_academicos.filter(
            id_universidad=id_universidad
        )

    programas_academicos = (
        programas_academicos.exclude(codigo_snies__in=["N/A", "", "No disponible"])
        .exclude(codigo_snies__isnull=True)
        .prefetch_related("admision")
        .all()
    )

    # programas_academicos = programas_academicos.all()

    print(programas_academicos)

    universidades = Universidad.objects.all()

    return render(
        request,
        "lista_programas.html",
        {
            "programas_academicos": programas_academicos,
            "busqueda": busqueda,
            "id_universidad": id_universidad,
            "universidades": universidades,
        },
    )


def detalle_programa(request, codigo_snies):
    # programa_academico = ProgramaAcademico.objects.get(codigo_snies=codigo_snies)
    programa_academico = get_object_or_404(
        ProgramaAcademico.objects.select_related("id_universidad__contacto"),
        codigo_snies=codigo_snies,
    )
    # admision = get_object_or_404(Admision, codigo_snies=programa_academico.codigo_snies)
    admision = Admision.objects.filter(
        codigo_snies=programa_academico.codigo_snies
    ).first()

    contacto = None
    if hasattr(programa_academico.id_universidad, "contacto"):
        # Si la universidad tiene un contacto, lo obtenemos
        contacto = programa_academico.id_universidad.contacto

    print(programa_academico)
    print(admision)
    print(contacto)

    return render(
        request,
        "detalle_programa.html",
        {
            "programa_academico": programa_academico,
            "admision": admision,
            "contacto": contacto,
        },
    )


def registro_usuario(request):
    return render(request, "signup.html", {"form": CustomUserCreationForm()})
