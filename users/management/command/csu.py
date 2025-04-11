from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(email="admin@mail.com")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("1234qwe")
        user.save()
