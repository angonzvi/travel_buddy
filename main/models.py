from django.db import models
import re
from datetime import date, datetime

# Create your models here.
#User Manager
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 2:
            errors['firstname_len'] = "nombre debe tener al menos 2 caracteres de largo";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombreporfavor"

        if len(postData['password']) < 4:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors

class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

#Trip Manager
class TripsManager(models.Manager):
  def validate(self, postData):
        today = str(date.today())
        errors = {}
        if len(postData['destination']) < 5:
            errors['empty_plan'] = "El destino debe tener mas de 5 letras"
        if len(postData['description_plan']) < 5:
            errors['empty_plan'] = "El plan debe tener mas de 5 letras"
        if postData['start_date'] < today :
            errors["start_date"] = "Verifique la fecha de ida. Debe ser mayor que la fecha actual"
        if postData['end_date'] < postData['start_date'] :
            errors["end_date"] = "La fecha de ida debe ser menor que la fecha de llegada"
        return errors

class Trips(models.Model):
    
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length=255)
    start_date = models.DateField(null = True, blank = True)
    end_date = models.DateField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    owner_user = models.ForeignKey(User, related_name = 'viajes_creados', on_delete = models.CASCADE, null = True, blank = True)
    user = models.ManyToManyField(User, related_name = 'viajes')

    objects = TripsManager()