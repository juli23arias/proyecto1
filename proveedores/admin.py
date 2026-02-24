from django.contrib import admin
from .models import Proveedor, TipoDocumento, Documento

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nit', 'nombre', 'email', 'telefono', 'fecha_registro', 'user')
    search_fields = ('nit', 'nombre', 'email')
    list_filter = ('fecha_registro',)

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'requiere_vencimiento')
    search_fields = ('nombre',)
    list_filter = ('requiere_vencimiento',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'tipo_documento', 'fecha_carga', 'fecha_vencimiento', 'estado')
    list_filter = ('tipo_documento', 'fecha_carga', 'estado')
    search_fields = ('proveedor__nombre', 'proveedor__nit')
    list_editable = ('estado',) # Allow quick editing of status
    readonly_fields = ('fecha_carga',)
    fields = ('proveedor', 'tipo_documento', 'archivo', 'fecha_vencimiento', 'fecha_carga', 'estado', 'comentario')
