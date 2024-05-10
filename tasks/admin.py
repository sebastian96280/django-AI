from django.contrib import admin
from .models import tTipe_document
from .models import tTipo_solicitud
from .models import tEstado_solicitud
from .models import tArea
from .models import tEstado_Activo
from .models import tformatoSolicitud


class TaskAdmin(admin.ModelAdmin):
    readonly_fields=("created",)

# Register your models here.
admin.site.register(tTipe_document)
admin.site.register(tTipo_solicitud) 
admin.site.register(tEstado_solicitud) 
admin.site.register(tArea) 
admin.site.register(tEstado_Activo)
admin.site.register(tformatoSolicitud)