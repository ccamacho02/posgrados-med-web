import os
import django
import pytest
from django.db import connection
from django.core.management.color import no_style
from django.db import models
from django.conf import settings

# Configurar Django para pruebas
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posgrados_med.settings")
django.setup()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Configuración personalizada de BD que crea las tablas no administradas
    """
    with django_db_blocker.unblock():
        # Habilitar extension `unaccent` si no está habilitada
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")
            except Exception as e:
                print(f"Error al crear la extensión unaccent: {e}")

        # Crear las tablas manualmente
        with connection.cursor() as cursor:

            # Tabla universidad
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS universidad (
                    id_universidad SERIAL PRIMARY KEY,
                    nombre_universidad VARCHAR(100) NOT NULL,
                    ciudad VARCHAR(100) NOT NULL
                );
            """
            )

            # Tabla programa_academico
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS programa_academico (
                    codigo_snies VARCHAR(15) PRIMARY KEY,
                    id_universidad INTEGER NOT NULL,
                    nombre_programa VARCHAR(100) NOT NULL,
                    duracion VARCHAR(50),
                    numero_cupos INTEGER,
                    periocidad_admisiones VARCHAR(50),
                    url VARCHAR(200),
                    titulo_otorgado VARCHAR(100),
                    total_creditos INTEGER,
                    FOREIGN KEY (id_universidad) REFERENCES universidad(id_universidad)
                );
            """
            )

            # Tabla contacto
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS contacto (
                    id_contacto SERIAL PRIMARY KEY,
                    id_universidad INTEGER NOT NULL,
                    telefono VARCHAR(15),
                    correo VARCHAR(100),
                    FOREIGN KEY (id_universidad) REFERENCES universidad(id_universidad)
                );
            """
            )

            # Tabla admision
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS admision (
                    id_admision VARCHAR(50) PRIMARY KEY,
                    codigo_snies VARCHAR(15) NOT NULL,
                    periodo VARCHAR(6) NOT NULL,
                    fecha_inicio_inscripcion DATE,
                    fecha_cierre_inscripcion DATE,
                    fecha_examen_admision DATE,
                    fecha_publicacion_admitidos DATE,
                    paso_a_paso VARCHAR(200),
                    precio_inscripcion INTEGER,
                    precio_semestre INTEGER,
                    FOREIGN KEY (codigo_snies) REFERENCES programa_academico(codigo_snies)
                );
            """
            )


@pytest.fixture(autouse=True)
def clean_db(django_db_setup, django_db_blocker):
    """
    Limpia las tablas después de cada prueba
    """
    yield
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM admision;")
            cursor.execute("DELETE FROM contacto;")
            cursor.execute("DELETE FROM programa_academico;")
            cursor.execute("DELETE FROM universidad;")


# Fixtures para datos de prueba
@pytest.fixture
def universidad_test(db):
    """Fixture para crear una universidad de prueba"""
    from catalogo.models import Universidad

    return Universidad.objects.create(
        id_universidad=1, nombre_universidad="Universidad de Pruebas", ciudad="Bogotá"
    )


@pytest.fixture
def universidad_cali(db):
    """Segunda universidad para pruebas de filtros"""
    from catalogo.models import Universidad

    return Universidad.objects.create(
        id_universidad=2, nombre_universidad="Universidad del Valle", ciudad="Cali"
    )


@pytest.fixture
def programa_cardiologia(universidad_test):
    """Programa de cardiología para pruebas"""
    from catalogo.models import ProgramaAcademico

    return ProgramaAcademico.objects.create(
        codigo_snies="12345",
        id_universidad=universidad_test,
        nombre_programa="Especialización en Cardiología",
        duracion="4 semestres",
        numero_cupos=20,
        url="https://test.edu.co/cardiologia",
        titulo_otorgado="Especialista en Cardiología",
        total_creditos=60,
    )


@pytest.fixture
def programa_neurologia(universidad_cali):
    """Programa de neurología para pruebas"""
    from catalogo.models import ProgramaAcademico

    return ProgramaAcademico.objects.create(
        codigo_snies="67890",
        id_universidad=universidad_cali,
        nombre_programa="Especialización en Neurología",
        duracion="4 semestres",
        numero_cupos=15,
        url="https://univalle.edu.co/neurologia",
        titulo_otorgado="Especialista en Neurología",
        total_creditos=64,
    )


@pytest.fixture
def programa_sin_snies(universidad_test):
    """Programa con SNIES inválido (debe ser excluido)"""
    from catalogo.models import ProgramaAcademico

    return ProgramaAcademico.objects.create(
        codigo_snies="",
        id_universidad=universidad_test,
        nombre_programa="Programa Sin SNIES",
        duracion="4 semestres",
    )


@pytest.fixture
def admision_cardiologia(programa_cardiologia):
    """Datos de admisión para cardiología"""
    from catalogo.models import Admision
    from datetime import date

    return Admision.objects.create(
        id_admision="202501-12345",
        codigo_snies=programa_cardiologia,
        periodo="202501",
        fecha_inicio_inscripcion=date(2025, 1, 15),
        fecha_cierre_inscripcion=date(2025, 2, 15),
        fecha_examen_admision=date(2025, 3, 1),
        precio_inscripcion=150000,
        precio_semestre=2500000,
    )
