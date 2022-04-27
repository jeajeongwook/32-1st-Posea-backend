from django.db import models

from cores.models import TimeStamp

class MainCategory(models.Model) :
    name = models.CharField(max_length=50)

    class Meta :
        db_table = 'maincategories'


class Category(models.Model) :
    name         = models.CharField(max_length=100)
    maincategory = models.ForeignKey('Main', on_delete=models.CASCADE)

    class Meta :
        db_table = 'categories'


class Product(TimeStamp) :
    category  = models.ForeignKey('Category', on_delete=models.CASCADE)
    name      = models.CharField(max_length=100)
    usage     = models.CharField(max_length=100)
    texture   = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    detail    = models.CharField(max_length=1000)
    is_new    = models.BooleanField(default=False)
    skins     = models.ManyToManyField('Skin', through="Product_Skin")
    scents    = models.ManyToManyField('Scent', through="Product_Scent")

    class Meta :
        db_table = 'products'


class ProductSkin(models.Model) : 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    skin    = models.ForeignKey('Skin', on_delete=models.CASCADE)

    class Meta :
        db_table = 'productskins'


class Skin(models.Model) :
    skin_type = models.CharField(max_length=30)

    class Meta :
        db_table = 'skins'


class ProductScent(models.Model) : 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    Scent   = models.ForeignKey('Scent', on_delete=models.CASCADE)

    class Meta :
        db_table = 'productscents'


class Scent(models.Model) :
    name = models.CharField(max_length=30)

    class Meta :
        db_table = 'scents'


class Image(models.Model) :
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    class Meta :
        db_table = 'images'


class Selection(models.Model) :
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.IntegerField()
    price   = models.DecimalField(max_digits = 10, decimal_places = 3)

    class Meta :
        db_table = 'selections'


class Ingredient(models.Model) :
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    detail_text = models.CharField(max_length=500)

    class Meta :
        db_table = 'ingredients'