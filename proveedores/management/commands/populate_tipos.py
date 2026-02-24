from django.core.management.base import BaseCommand
from proveedores.models import TipoDocumento

class Command(BaseCommand):
    help = 'Populates initial TipoDocumento data'

    def handle(self, *args, **kwargs):
        tipos = [
            {'nombre': 'Planilla Seguridad Social', 'requiere_vencimiento': True},
            {'nombre': 'Política SST', 'requiere_vencimiento': False},
            {'nombre': 'Exámenes médicos ocupacionales', 'requiere_vencimiento': True},
            {'nombre': 'ARL', 'requiere_vencimiento': True},
            {'nombre': 'Certificado EPS', 'requiere_vencimiento': True},
            {'nombre': 'Certificado Pensión', 'requiere_vencimiento': True},
            {'nombre': 'Certificado laboral', 'requiere_vencimiento': True},
            {'nombre': 'Otros requisitos SST', 'requiere_vencimiento': False},
        ]

        for tipo_data in tipos:
            TipoDocumento.objects.get_or_create(
                nombre=tipo_data['nombre'],
                defaults={'requiere_vencimiento': tipo_data['requiere_vencimiento']}
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully checked/created "{tipo_data["nombre"]}"'))
