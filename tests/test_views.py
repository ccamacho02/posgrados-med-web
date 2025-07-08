import pytest
from django.urls import reverse
from django.test import Client
from catalogo.models import Universidad, ProgramaAcademico, Admision
from datetime import date


@pytest.mark.django_db
class TestListaProgramas:

    def test_lista_programas(self, clean_db, programa_cardiologia, programa_neurologia):
        """Prueba que la lista muestre los programas académicos válidos"""
        client = Client()
        response = client.get(reverse("lista_programas"))

        assert response.status_code == 200
        assert "programas_academicos" in response.context
        assert "universidades" in response.context

        # Debe mostrar 2 programas (excluyendo el que no tiene SNIES)
        programas = response.context["programas_academicos"]
        assert len(programas) == 2

        # Verificar que estén ambos programas
        nombres_programas = [programa.nombre_programa for programa in programas]
        assert programa_cardiologia.nombre_programa in nombres_programas
        assert programa_neurologia.nombre_programa in nombres_programas

    def test_busqueda_por_nombre_programa(
        self, clean_db, programa_cardiologia, programa_neurologia
    ):
        """Prueba que la búsqueda por nombre de programa funcione correctamente"""
        client = Client()
        response = client.get(reverse("lista_programas"), {"busqueda": "Cardiología"})

        assert response.status_code == 200
        programas = response.context["programas_academicos"]
        assert len(programas) == 1
        assert programas[0].nombre_programa == programa_cardiologia.nombre_programa

    def test_busqueda_sin_resultados(self, clean_db, programa_cardiologia):
        """Prueba que la búsqueda sin resultados retorne una lista vacía"""
        client = Client()
        response = client.get(reverse("lista_programas"), {"busqueda": "Inexistente"})

        assert response.status_code == 200
        programas = response.context["programas_academicos"]
        assert len(programas) == 0
        assert response.context["busqueda"] == "Inexistente"

    def test_busqueda_case_insensitive(self, clean_db, programa_cardiologia):
        """Prueba que la búsqueda sea insensible a mayúsculas y minúsculas"""
        client = Client()

        # Búsqueda con minusculas
        response = client.get(reverse("lista_programas"), {"busqueda": "cardiología"})
        assert response.status_code == 200
        assert len(response.context["programas_academicos"]) == 1

        # Búsqueda con mayúsculas
        response = client.get(reverse("lista_programas"), {"busqueda": "CARDIOLOGÍA"})
        assert response.status_code == 200
        assert len(response.context["programas_academicos"]) == 1

    def test_filtro_por_universidad(
        self, clean_db, universidad_test, programa_cardiologia, programa_neurologia
    ):
        """Prueba que el filtro por universidad funcione correctamente"""
        client = Client()
        response = client.get(
            reverse("lista_programas"),
            {"id_universidad": universidad_test.id_universidad},
        )

        assert response.status_code == 200
        programas = response.context["programas_academicos"]
        assert len(programas) == 1
        assert programas[0].nombre_programa == programa_cardiologia.nombre_programa
        assert (
            programas[0].id_universidad.id_universidad
            == universidad_test.id_universidad
        )

    def test_filtros_combinados(
        self, clean_db, programa_cardiologia, programa_neurologia, universidad_test
    ):
        """Prueba que los filtros combinados funcionen correctamente"""
        client = Client()
        response = client.get(
            reverse("lista_programas"),
            {
                "busqueda": "Especialización",
                "id_universidad": universidad_test.id_universidad,
            },
        )

        assert response.status_code == 200
        programas = response.context["programas_academicos"]
        assert len(programas) == 1
        assert programas[0].nombre_programa == programa_cardiologia.nombre_programa

    def test_exlusion_snies_invalidos(
        self, clean_db, programa_sin_snies, programa_cardiologia
    ):
        client = Client()
        response = client.get(reverse("lista_programas"))

        programas = response.context["programas_academicos"]
        codigo_snies = [programa.codigo_snies for programa in programas]
        assert len(programas) == 1  # Solo debe quedar el programa con SNIES
        assert programa_sin_snies.codigo_snies not in codigo_snies
        assert programa_cardiologia.codigo_snies in codigo_snies

    def test_parametros_vacios(
        self, clean_db, programa_cardiologia, programa_neurologia
    ):
        """Prueba que la lista muestre todos los programas si no hay filtros"""
        client = Client()
        response = client.get(
            reverse("lista_programas"), {"busqueda": "", "id_universidad": ""}
        )

        assert response.status_code == 200
        programas = response.context["programas_academicos"]
        assert len(programas) == 2


# class TestDetallePrograma:

#     def test_detalle_programa(
#         self, clean_db, programa_cardiologia, admision_cardiologia
#     ):
#         """Prueba que el detalle del programa muestre la información correcta"""
#         client = Client()
#         response = client.get(
#             reverse("detalle_programa", args=[programa_cardiologia.codigo_snies])
#         )

#         assert response.status_code == 200
#         assert "programa_academico" in response.context
#         assert "admision" in response.context

#         programa = response.context["programa_academico"]
#         admision = response.context["admision"]

#         assert programa.codigo_snies == programa_cardiologia.codigo_snies
#         assert programa.nombre_programa == programa_cardiologia.nombre_programa
#         assert admision.codigo_snies.codigo_snies == programa_cardiologia.codigo_snies
