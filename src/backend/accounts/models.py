import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from accounts.meter_number import generate_meter_number


class UserAccountManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **kwargs):
        """
        Creates and saves a User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError("Users must have a phone number ")
        
        # email = self.normalize_email(email)
        # email = email.lower()

        user = self.model(
            phone_number=phone_number,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **kwargs):
        """
        Creates and saves a superuser with the given phone_number and password.
        """
        user = self.create_user(
            phone_number,
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True, null=True
    )
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=13, null=True, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class AccountMeter(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='meter_details')
    meter_number = models.PositiveBigIntegerField(null=True, unique=True, editable=False)
    v_rating = models.PositiveSmallIntegerField(null=True, default=240)
    c_rating = models.PositiveSmallIntegerField(null=True, default=10)
    location = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.meter_number)
    
    def save(self, *args, **kwargs):
        if not self.meter_number:
            # Get existing meter numbers
            existing_numbers = set(AccountMeter.objects.values_list('meter_number', flat=True))
            # Generate a unique meter number
            self.meter_number = generate_meter_number(existing_numbers)
        super().save(*args, **kwargs)
    