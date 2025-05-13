from django.contrib import admin
from .models import Universidad, ProgramaAcademico, Contacto, Admision

# Register your models here.
admin.site.register(Universidad)
admin.site.register(ProgramaAcademico)
admin.site.register(Contacto)
admin.site.register(Admision)