from django.db import models

from cores.models import TimeStamp

# Create your models here.
class User(TimeStamp) :
    first_name   = models.CharField(max_length=10)
    last_name    = models.CharField(max_length=30)
    email        = models.EmailField(max_length=150, unique=True)
    password     = models.CharField(max_length=200)
  
    class Meta :
        db_table = 'users'