from django import forms
from .models import Proveedor, Documento

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nit', 'nombre', 'email', 'telefono']
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 900.123.456-1'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o Razón Social'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contacto@empresa.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'archivo', 'fecha_vencimiento', 'enviado_a_proveedor', 'descripcion']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}), # Bootstrap 5 class
            'archivo': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción opcional del documento'}),
        }
        labels = {
            'tipo_documento': 'Seleccione el tipo de documento',
            'fecha_vencimiento': 'Fecha de Vencimiento (Si aplica)',
            'enviado_a_proveedor': '¿Enviar inmediatamente al proveedor?',
        }

class AdminDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['proveedor', 'tipo_documento', 'archivo', 'fecha_vencimiento', 'enviado_a_proveedor', 'descripcion']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'enviado_a_proveedor': '¿Enviar al proveedor?',
        }

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo and not archivo.name.endswith('.pdf'):
            raise forms.ValidationError("Solo se permiten archivos PDF.")
        return archivo
