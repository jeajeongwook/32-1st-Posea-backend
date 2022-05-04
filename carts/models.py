from django.db import models

from products.models import Product
from users.models import User
from cores.models import TimeStamp

# Create your models here.

class Cart(TimeStamp):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count   = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'carts'