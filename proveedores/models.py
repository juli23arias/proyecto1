from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Proveedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='proveedor', null=True, blank=True)
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    nombre = models.CharField(max_length=100, verbose_name="Nombre o Razón Social")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.nombre} ({self.nit})"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


from datetime import date

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Tipo de Documento")
    requiere_vencimiento = models.BooleanField(default=True, verbose_name="Requiere Vencimiento")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"


class Documento(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    REMITENTE_CHOICES = [
        ('admin', 'Administración'),
        ('proveedor', 'Proveedor'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, verbose_name="Tipo de Documento")
    archivo = models.FileField(
        upload_to='documentos/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="Archivo (PDF)"
    )
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Carga")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento", null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
    enviado_a_proveedor = models.BooleanField(default=False, verbose_name="Enviado al Proveedor")
    subido_por = models.CharField(max_length=20, choices=REMITENTE_CHOICES, default='proveedor', verbose_name="Subido por")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentario del Administrador")

    def __str__(self):
        return f"{self.tipo_documento} - {self.proveedor} ({self.get_estado_display()})"
    
    def esta_vencido(self):
        """Retorna True si el documento tiene fecha de vencimiento y ya pasó."""
        if self.fecha_vencimiento:
            return self.fecha_vencimiento < date.today()
        return False

    def es_valido(self):
        """
        Retorna False si:
        - El estado es RECHAZADO
        - El documento está vencido
        En cualquier otro caso (Pendiente o Aprobado y vigente) retorna True.
        """
        if self.estado == 'rechazado':
            return False
        if self.esta_vencido():
            return False
        return True

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
