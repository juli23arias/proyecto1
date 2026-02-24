from django.urls import path
from .views import (
    DashboardView,
    ProveedorListView, ProveedorCreateView, 
    ProveedorDetailView, DocumentoCreateView,
    serve_document_pdf
)
from .supplier_views import SupplierDashboardView, SupplierDocumentUploadView, SupplierReceivedDocumentsView

urlpatterns = [
    # Rutas para el Administrador
    path('', DashboardView.as_view(), name='dashboard'),
    path('listado/', ProveedorListView.as_view(), name='proveedor_list'),
    path('nuevo/', ProveedorCreateView.as_view(), name='proveedor_add'),
    path('<int:pk>/', ProveedorDetailView.as_view(), name='proveedor_detail'),
    path('<int:pk>/documento/nuevo/', DocumentoCreateView.as_view(), name='documento_add'),

    # Rutas para el Proveedor (NUEVAS)
    path('proveedor/dashboard/', SupplierDashboardView.as_view(), name='proveedor_dashboard'),
    path('proveedor/documento/nuevo/', SupplierDocumentUploadView.as_view(), name='supplier_document_add'),
    path('proveedor/documentos/recibidos/', SupplierReceivedDocumentsView.as_view(), name='supplier_received_documents'),
    
    # Visualizador de PDF (SAMEORIGIN para evitar bloqueo de iframe)
    path('view-pdf/<int:pk>/', serve_document_pdf, name='serve_document_pdf'),
]
