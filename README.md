# YSG Gestor Documental (Sprint 1)

Sistema web para el control de requisitos legales de proveedores. Desarrollado con Django y SQLite.

## Requerimientos
- Python 3.8+
- Django 5.x

## Instalación

1. **Crear entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Instalar dependencias:**
   ```bash
   pip install django
   ```

3. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

4. **Crear superusuario (para acceder al admin):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Ejecutar el servidor:**
   ```bash
   python manage.py runserver
   ```

## Uso

1. Acceder a `http://127.0.0.1:8000/` para ver el listado de proveedores.
2. Acceder a `http://127.0.0.1:8000/admin/` para gestionar Tipos de Documento iniciales (Ej: "Planilla de seguridad social", "Política de seguridad", "Exámenes médicos").
3. Registrar proveedores y cargar sus documentos PDF.
