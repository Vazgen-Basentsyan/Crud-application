from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', "admin")
        extra_fields.setdefault('last_name', "admin")
        extra_fields.setdefault('age', "100")
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.PositiveIntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Home(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    land_sqm = models.FloatField()
    place_sqm = models.FloatField()
    bedrooms = models.PositiveIntegerField()

    def __str__(self):
        return "{} : {}".format(self.user.email,  self.title)


class HomeImage(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
