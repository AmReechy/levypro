from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class PayeeManager(BaseUserManager):
    def create_user(self, id_number, phone_number, password=None, **extra):
        if not id_number or not phone_number:
            raise ValueError("ID number and phone number required")

        user = self.model(
            id_number=id_number,
            phone_number=phone_number,
            **extra
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, id_number, phone_number, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(id_number, phone_number, password, **extra)


class Payee(AbstractBaseUser, PermissionsMixin):
    ID_TYPES = [
        ("NIN", "NIN"),
        ("TIN", "TIN"),
        ("BVN", "BVN"),
        ("PHONE", "Phone Number"),
    ]

    id_type = models.CharField(max_length=10, choices=ID_TYPES)
    id_number = models.CharField(max_length=50, unique=True, default='123456789')
    phone_number = models.CharField(max_length=15, default='123456789')
    email = models.EmailField(unique=True, default='user@example.com')

    full_name = models.CharField(max_length=200, default='John Doe')
    date_of_birth = models.DateField(null=True)
    address = models.TextField()
    occupation = models.CharField(max_length=100, default="Worker")
    passport_photo = models.ImageField(upload_to="passports/")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PayeeManager()

    USERNAME_FIELD = "id_number"
    REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return self.full_name
