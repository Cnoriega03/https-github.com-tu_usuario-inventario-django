import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea o actualiza un superusuario usando variables de entorno."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "No se creo superusuario: faltan DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        call_command("configurar_permisos", admin_user=username)

        action = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' {action} correctamente."))
