from django.urls import path
from . import admin_views

urlpatterns = [
    # Dashboard eliminado, usamos la ruta raíz '/'

    
    # Usuarios
    path('usuarios/', admin_views.AdminUserListView.as_view(), name='admin_user_list'),
    path('usuarios/nuevo/', admin_views.AdminUserCreateView.as_view(), name='admin_user_create'),
    path('usuarios/<int:pk>/editar/', admin_views.AdminUserUpdateView.as_view(), name='admin_user_update'),
    path('usuarios/<int:pk>/eliminar/', admin_views.AdminUserDeleteView.as_view(), name='admin_user_delete'),

    # Stats
    path('estadisticas/', admin_views.AdminStatsView.as_view(), name='admin_stats'),
    
    # Categorías
    path('categorias/', admin_views.AdminCategoryListView.as_view(), name='admin_category_list'),
    path('categorias/nueva/', admin_views.AdminCategoryCreateView.as_view(), name='admin_category_create'),
    path('categorias/<int:pk>/editar/', admin_views.AdminCategoryUpdateView.as_view(), name='admin_category_update'),
    path('categorias/<int:pk>/eliminar/', admin_views.AdminCategoryDeleteView.as_view(), name='admin_category_delete'),
    
    # Documentos
    path('documentos/', admin_views.AdminDocumentListView.as_view(), name='admin_document_list'),
    path('documentos/nuevo/', admin_views.AdminDocumentCreateView.as_view(), name='admin_document_create'),
    path('documentos/enviados/', admin_views.AdminDocumentOutboxView.as_view(), name='admin_document_outbox'),
    path('documentos/enviados/nuevo/', admin_views.AdminOutboxCreateView.as_view(), name='admin_document_outbox_create'),
    path('documentos/<int:pk>/revisar/', admin_views.AdminDocumentUpdateView.as_view(), name='admin_document_review'),
]
