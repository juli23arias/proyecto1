from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Proveedor, Documento
from .forms import ProveedorForm, DocumentoForm
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .mixins import AdminRequiredMixin

class DashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'proveedores/admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Totales (Solo documentos de proveedores para requisitos legales)
        context['total_users'] = User.objects.count()
        context['total_proveedores'] = Proveedor.objects.count()
        context['total_documentos'] = Documento.objects.filter(subido_por='proveedor').count()
        
        # Documentos Status (Excluyendo mensajería administrativa)
        from datetime import date
        context['docs_vencidos'] = Documento.objects.filter(
            subido_por='proveedor',
            fecha_vencimiento__lt=date.today()
        ).count()
        
        context['docs_pendientes'] = Documento.objects.filter(subido_por='proveedor', estado='pendiente').count()
        context['docs_aprobados'] = Documento.objects.filter(subido_por='proveedor', estado='aprobado').count()
        context['docs_rechazados'] = Documento.objects.filter(subido_por='proveedor', estado='rechazado').count()

        return context
    
class ProveedorListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Proveedor
    template_name = 'proveedores/proveedor_list.html'
    context_object_name = 'proveedores'
    ordering = ['-fecha_registro']

class ProveedorCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

    def form_valid(self, form):
        messages.success(self.request, "Proveedor registrado exitosamente.")
        return super().form_valid(form)

class ProveedorDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Proveedor
    template_name = 'proveedores/proveedor_detail.html'
    context_object_name = 'proveedor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mostrar solo documentos cargados por el proveedor (sus requerimientos legales)
        context['documentos_proveedor'] = self.object.documentos.filter(subido_por='proveedor').order_by('-fecha_carga')
        return context

class DocumentoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'proveedores/documento_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.proveedor = get_object_or_404(Proveedor, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedor'] = self.proveedor
        return context

    def form_valid(self, form):
        form.instance.proveedor = self.proveedor
        form.instance.subido_por = 'admin'
        messages.success(self.request, "Documento cargado exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('proveedor_detail', kwargs={'pk': self.proveedor.pk})
    

from django.http import FileResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin

@xframe_options_sameorigin
def serve_document_pdf(request, pk):
    """
    Sirve el archivo PDF de un documento permitiendo su visualización en iframes 
    del mismo origen (SAMEORIGIN), solucionando el bloqueo de seguridad.
    """
    documento = get_object_or_404(Documento, pk=pk)
    return FileResponse(documento.archivo, content_type='application/pdf')
