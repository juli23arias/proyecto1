from django import forms
from django.contrib.auth.models import User
from proveedores.models import Proveedor

class ProveedorRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Usuario para iniciar sesión")
    password = forms.CharField(widget=forms.PasswordInput, help_text="Contraseña segura")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = Proveedor
        fields = ['nit', 'nombre', 'telefono']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
