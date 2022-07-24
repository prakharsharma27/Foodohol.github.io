# from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .manager import CustomUserManager


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'dob']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default="")
    mealType = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    cuisine = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    product_id = models.AutoField
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.IntegerField(max_length=10, default="")
    Query = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000, default="")
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)

    def __str__(self):
        return self.name
