from django.db import models


# Create your models here.
class Universidad(models.Model):
    id_universidad = models.AutoField(primary_key=True)
    nombre_universidad = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "universidad"

    def __str__(self):
        return self.nombre_universidad


class Contacto(models.Model):
    id_contacto = models.AutoField(primary_key=True)
    id_universidad = models.OneToOneField(
        Universidad,
        on_delete=models.CASCADE,
        db_column="id_universidad",
        related_name="contacto",
    )
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "contacto"

    def __str__(self):
        return f"Contacto de {self.id_universidad.nombre_universidad} - {self.telefono}"


class ProgramaAcademico(models.Model):
    codigo_snies = models.CharField(primary_key=True, max_length=15)
    id_universidad = models.ForeignKey(
        Universidad, on_delete=models.CASCADE, db_column="id_universidad"
    )
    nombre_programa = models.CharField(max_length=100)
    duracion = models.CharField(max_length=50, blank=True, null=True)
    numero_cupos = models.IntegerField(blank=True, null=True)
    periocidad_admisiones = models.CharField(max_length=50, blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    titulo_otorgado = models.CharField(max_length=100, blank=True, null=True)
    total_creditos = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "programa_academico"

    def __str__(self):
        return f"{self.nombre_programa} - {self.id_universidad.nombre_universidad}"


class Admision(models.Model):
    id_admision = models.CharField(primary_key=True, max_length=50)
    codigo_snies = models.ForeignKey(
        ProgramaAcademico,
        on_delete=models.CASCADE,
        db_column="codigo_snies",
        related_name="admision",
    )
    periodo = models.CharField(max_length=6)
    fecha_inicio_inscripcion = models.DateField(blank=True, null=True)
    fecha_cierre_inscripcion = models.DateField(blank=True, null=True)
    fecha_examen_admision = models.DateField(blank=True, null=True)
    fecha_publicacion_admitidos = models.DateField(blank=True, null=True)
    paso_a_paso = models.CharField(max_length=200, blank=True, null=True)
    precio_inscripcion = models.IntegerField(blank=True, null=True)
    precio_semestre = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "admision"

    def __str__(self):
        return f"Admisión {self.codigo_snies.nombre_programa} - {self.fecha_inicio_inscripcion} a {self.fecha_cierre_inscripcion}"
