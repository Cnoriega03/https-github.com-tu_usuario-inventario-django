from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea grupos de permisos para administradores y usuarios normales del inventario."

    def add_arguments(self, parser):
        parser.add_argument(
            "--admin-user",
            help="Usuario existente que sera marcado como staff y agregado al grupo Administrador.",
        )
        parser.add_argument(
            "--inventory-user",
            help="Usuario existente que sera marcado como no staff y agregado al grupo Usuario Inventario.",
        )

    def handle(self, *args, **options):
        grupo_admin = self._crear_grupo_administrador()
        grupo_usuario = self._crear_grupo_usuario_inventario()

        if options.get("admin_user"):
            self._asignar_admin(options["admin_user"], grupo_admin)

        if options.get("inventory_user"):
            self._asignar_usuario_inventario(options["inventory_user"], grupo_usuario)

        self.stdout.write(self.style.SUCCESS("Grupos y permisos configurados correctamente."))
        self.stdout.write("- Administrador: puede entrar al admin, crear usuarios y gestionar todo el inventario.")
        self.stdout.write("- Usuario Inventario: no puede entrar al admin; solo usa las pantallas del inventario.")

    def _crear_grupo_administrador(self):
        grupo, _ = Group.objects.get_or_create(name="Administrador")
        permisos = Permission.objects.filter(
            content_type__app_label__in=["inventario", "auth"],
            codename__in=[
                "add_categoria",
                "change_categoria",
                "delete_categoria",
                "view_categoria",
                "add_producto",
                "change_producto",
                "delete_producto",
                "view_producto",
                "add_movimientoinventario",
                "change_movimientoinventario",
                "delete_movimientoinventario",
                "view_movimientoinventario",
                "puede_ver_alertas",
                "add_user",
                "change_user",
                "delete_user",
                "view_user",
                "add_group",
                "change_group",
                "delete_group",
                "view_group",
            ],
        )
        grupo.permissions.set(permisos)
        return grupo

    def _crear_grupo_usuario_inventario(self):
        grupo, _ = Group.objects.get_or_create(name="Usuario Inventario")
        permisos = Permission.objects.filter(
            content_type__app_label="inventario",
            codename__in=[
                "view_categoria",
                "add_categoria",
                "change_categoria",
                "view_producto",
                "add_producto",
                "change_producto",
                "view_movimientoinventario",
                "add_movimientoinventario",
                "puede_ver_alertas",
            ],
        )
        grupo.permissions.set(permisos)
        return grupo

    def _asignar_admin(self, username, grupo):
        usuario = self._obtener_usuario(username)
        usuario.is_staff = True
        usuario.groups.add(grupo)
        usuario.save(update_fields=["is_staff"])
        self.stdout.write(self.style.SUCCESS(f"Usuario '{username}' asignado como Administrador."))

    def _asignar_usuario_inventario(self, username, grupo):
        usuario = self._obtener_usuario(username)
        usuario.is_staff = False
        usuario.is_superuser = False
        usuario.groups.add(grupo)
        usuario.save(update_fields=["is_staff", "is_superuser"])
        self.stdout.write(self.style.SUCCESS(f"Usuario '{username}' asignado como Usuario Inventario."))

    def _obtener_usuario(self, username):
        User = get_user_model()
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(f"No existe un usuario con username '{username}'.") from exc
