from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Documento, Proveedor
from .forms import DocumentoForm
from .mixins import SupplierRequiredMixin

class SupplierDashboardView(LoginRequiredMixin, SupplierRequiredMixin, ListView):
    model = Documento
    template_name = 'proveedores/supplier_dashboard.html'
    context_object_name = 'documentos'

    def get_queryset(self):
        # Mostrar documentos CARGADOS por el proveedor (sus requerimientos legales)
        return Documento.objects.filter(
            proveedor__user=self.request.user,
            subido_por='proveedor'
        ).order_by('-fecha_carga')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedor'] = self.request.user.proveedor
        return context

class SupplierDocumentUploadView(LoginRequiredMixin, SupplierRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'proveedores/supplier_document_form.html'
    success_url = reverse_lazy('proveedor_dashboard')

    def form_valid(self, form):
        form.instance.proveedor = self.request.user.proveedor
        form.instance.subido_por = 'proveedor'
        # Los documentos subidos por el proveedor son siempre visibles para él
        form.instance.enviado_a_proveedor = True
        messages.success(self.request, "Documento cargado exitosamente.")
        return super().form_valid(form)

class SupplierReceivedDocumentsView(LoginRequiredMixin, SupplierRequiredMixin, ListView):
    model = Documento
    template_name = 'proveedores/received_documents.html'
    context_object_name = 'documentos'

    def get_queryset(self):
        # Mostrar documentos ENVIADOS por la administración AL proveedor
        return Documento.objects.filter(
            proveedor__user=self.request.user,
            subido_por='admin',
            enviado_a_proveedor=True
        ).order_by('-fecha_carga')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedor'] = self.request.user.proveedor
        return context
