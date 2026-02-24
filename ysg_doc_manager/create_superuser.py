import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ysg_doc_manager.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "admin@email.com"
password = "Admin123456"

if not User.objects.filter(username=username).exists():
    print("Creando superusuario...")
    User.objects.create_superuser(username, email, password)
else:
    print("El superusuario ya existe")