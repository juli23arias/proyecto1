from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Documento, Proveedor, TipoDocumento
from .forms import AdminDocumentUploadForm
from .mixins import AdminRequiredMixin

# --- USERS ---

class AdminUserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'proveedores/admin/user_list.html'
    context_object_name = 'users'
    ordering = ['-date_joined']


class AdminUserCreateView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'proveedores/admin/user_create_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        rol = request.POST.get('rol', 'proveedor')  # 'admin' or 'proveedor'

        errors = []
        if not username:
            errors.append('El nombre de usuario es obligatorio.')
        if not password or len(password) < 6:
            errors.append('La contrasena debe tener al menos 6 caracteres.')
        if User.objects.filter(username=username).exists():
            errors.append('Ya existe un usuario con ese nombre.')

        if errors:
            return render(request, self.template_name, {'errors': errors, 'form_data': request.POST})

        user = User.objects.create_user(username=username, email=email, password=password)

        if rol == 'admin':
            user.is_staff = True
            user.save()
        else:
            # Proveedor: crear perfil basico con datos minimos
            nit = request.POST.get('nit', '').strip() or f'NIT-{user.id}'
            nombre = request.POST.get('nombre_empresa', '').strip() or username
            telefono = request.POST.get('telefono', '').strip() or 'Sin telefono'
            Proveedor.objects.create(
                user=user,
                nit=nit,
                nombre=nombre,
                email=email,
                telefono=telefono,
            )

        messages.success(request, f'Usuario "{username}" creado exitosamente como {"Administrador" if rol == "admin" else "Proveedor"}.')
        return redirect('admin_user_list')


class AdminUserUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'proveedores/admin/user_form.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # Determine current role
        current_rol = 'admin' if user.is_staff else 'proveedor'
        return render(request, self.template_name, {'object': user, 'current_rol': current_rol})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        email = request.POST.get('email', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        rol = request.POST.get('rol', 'proveedor')

        user.email = email
        user.is_active = is_active

        if rol == 'admin':
            user.is_staff = True
            # Remove proveedor profile if switching to admin
            if hasattr(user, 'proveedor'):
                user.proveedor.delete()
        else:
            user.is_staff = False
            # Create proveedor profile if it doesn't exist
            if not hasattr(user, 'proveedor'):
                Proveedor.objects.create(
                    user=user,
                    nit=f'NIT-{user.id}',
                    nombre=user.username,
                    email=user.email or 'sin@email.com',
                    telefono='Sin telefono',
                )

        new_password = request.POST.get('new_password', '').strip()
        if new_password:
            if len(new_password) < 6:
                messages.error(request, 'La nueva contrasena debe tener al menos 6 caracteres.')
                return redirect('admin_user_update', pk=pk)
            user.set_password(new_password)

        user.save()
        messages.success(request, f'Usuario "{user.username}" actualizado exitosamente.')
        return redirect('admin_user_list')


class AdminUserDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, 'No puedes eliminar tu propio usuario.')
            return redirect('admin_user_list')
        username = user.username
        user.delete()
        messages.success(request, f'Usuario "{username}" eliminado exitosamente.')
        return redirect('admin_user_list')

class AdminStatsView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'proveedores/admin/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Detailed Stats
        context['total_users'] = User.objects.count()
        context['users_admin'] = User.objects.filter(is_staff=True).count()
        context['users_proveedor'] = User.objects.filter(groups__name='PROVEEDOR').count()
        
        context['docs_by_type'] = Documento.objects.filter(subido_por='proveedor').values('tipo_documento__nombre').annotate(total=Count('id'))
        context['docs_by_status'] = Documento.objects.filter(subido_por='proveedor').values('estado').annotate(total=Count('id'))
        
        return context

# --- CATEGORIES ---
class AdminCategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = TipoDocumento
    template_name = 'proveedores/admin/category_list.html'
    context_object_name = 'categorias'

class AdminCategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TipoDocumento
    fields = ['nombre', 'requiere_vencimiento']
    template_name = 'proveedores/admin/category_form.html'
    success_url = reverse_lazy('admin_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Categoría creada exitosamente.")
        return super().form_valid(form)

class AdminCategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = TipoDocumento
    fields = ['nombre', 'requiere_vencimiento']
    template_name = 'proveedores/admin/category_form.html'
    success_url = reverse_lazy('admin_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Categoría actualizada exitosamente.")
        return super().form_valid(form)

class AdminCategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = TipoDocumento
    template_name = 'proveedores/admin/category_confirm_delete.html'
    success_url = reverse_lazy('admin_category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Categoría eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

# --- DOCUMENTS ---
class AdminDocumentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Documento
    template_name = 'proveedores/admin/document_list.html'
    context_object_name = 'documentos'
    paginate_by = 20
    ordering = ['-fecha_carga']

    def get_queryset(self):
        # Mostrar solo documentos cargados por proveedores (sus requerimientos legales)
        queryset = Documento.objects.filter(subido_por='proveedor')
        
        # Filtros
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(proveedor__nombre__icontains=q) | 
                Q(proveedor__nit__icontains=q) |
                Q(tipo_documento__nombre__icontains=q)
            )
        
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
            
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_documento_id=tipo)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = TipoDocumento.objects.all()
        # Mejores prácticas: pasar filtros actuales al contexto
        context['q_actual'] = self.request.GET.get('q', '')
        context['estado_actual'] = self.request.GET.get('estado', '')
        tipo = self.request.GET.get('tipo', '')
        context['tipo_actual'] = int(tipo) if tipo and tipo.isdigit() else ''
        return context

class AdminDocumentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Documento
    fields = ['estado', 'comentario']
    template_name = 'proveedores/admin/document_review.html'
    success_url = reverse_lazy('admin_document_list')

    def form_valid(self, form):
        messages.success(self.request, "Estado del documento actualizado.")
        return super().form_valid(form)

class AdminDocumentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Documento
    form_class = AdminDocumentUploadForm
    template_name = 'proveedores/documento_form.html'
    success_url = reverse_lazy('admin_document_list')

    def form_valid(self, form):
        form.instance.subido_por = 'admin'
        messages.success(self.request, "Documento cargado y asignado exitosamente.")
        return super().form_valid(form)

class AdminDocumentOutboxView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Documento
    template_name = 'proveedores/admin/document_outbox.html'
    context_object_name = 'documentos'
    paginate_by = 20

    def get_queryset(self):
        # Solamente mostrar documentos que el admin ha enviado ACTIVAMENTE a proveedores
        queryset = Documento.objects.filter(
            subido_por='admin',
            enviado_a_proveedor=True
        )

        # Filtros
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(proveedor__nombre__icontains=q) |
                Q(proveedor__nit__icontains=q) |
                Q(tipo_documento__nombre__icontains=q)
            )

        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_documento_id=tipo)

        return queryset.order_by('-fecha_carga')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_envios'] = self.get_queryset().count()
        context['categorias'] = TipoDocumento.objects.all()
        context['q_actual'] = self.request.GET.get('q', '')
        tipo = self.request.GET.get('tipo', '')
        context['tipo_actual'] = int(tipo) if tipo and tipo.isdigit() else ''
        return context

class AdminOutboxCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Documento
    form_class = AdminDocumentUploadForm
    template_name = 'proveedores/admin/admin_outbox_form.html'
    success_url = reverse_lazy('admin_document_outbox')

    def form_valid(self, form):
        form.instance.subido_por = 'admin'
        # ensure it's sent to provider if uploaded from outbox
        form.instance.enviado_a_proveedor = True
        messages.success(self.request, "Documento enviado exitosamente al proveedor.")
        return super().form_valid(form)
