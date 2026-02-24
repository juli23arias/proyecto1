from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import ProveedorRegistrationForm
from django.contrib.auth import login

def register_proveedor(request):
    if request.method == 'POST':
        form = ProveedorRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Crear Usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            
            # 2. Asignar Grupo PROVEEDOR
            group, created = Group.objects.get_or_create(name='PROVEEDOR')
            user.groups.add(group)

            # 3. Crear Perfil Proveedor
            proveedor = form.save(commit=False)
            proveedor.user = user
            proveedor.email = user.email # Asegurar consistencia
            proveedor.save()

            messages.success(request, "Cuenta creada exitosamente. Bienvenido.")
            login(request, user)
            return redirect('proveedor_dashboard') # Redirigir al dashboard del proveedor
            
    else:
        form = ProveedorRegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})

def login_dispatch(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('dashboard') # Dashboard Admin
    elif request.user.groups.filter(name='PROVEEDOR').exists() or hasattr(request.user, 'proveedor'):
        return redirect('proveedor_dashboard')
    else:
        return redirect('dashboard') # Default fallback
