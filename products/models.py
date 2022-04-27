from django.db import models

from cores.models import TimeStamp

class MainCategory(models.Model) :
    name = models.CharField(max_length=50)

    class Meta :
        db_table = 'maincategories'


class Category(models.Model) :
    name         = models.CharField(max_length=100)
    maincategory = models.ForeignKey('MainCategory', on_delete=models.CASCADE)

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
    skins     = models.ManyToManyField('Skin', through="ProductSkin")
    scents    = models.ManyToManyField('Scent', through="ProductScent")

    class Meta :
        db_table = 'products'


class ProductSkin(models.Model) : 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    skin    = models.ForeignKey('Skin', on_delete=models.CASCADE, null=True)

    class Meta :
        db_table = 'product_skins'


class Skin(models.Model) :
    skin_type = models.CharField(max_length=30)

    class Meta :
        db_table = 'skins'


class ProductScent(models.Model) : 
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    Scent   = models.ForeignKey('Scent', on_delete=models.CASCADE)

    class Meta :
        db_table = 'product_scents'


class Scent(models.Model) :
    name = models.CharField(max_length=30)

    class Meta :
        db_table = 'scents'


class ProductImage(models.Model) :
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    class Meta :
        db_table = 'product_images'


class Selection(models.Model) :
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.IntegerField()
    price   = models.DecimalField(max_digits = 11, decimal_places = 3)

    class Meta :
        db_table = 'selections'


class Ingredient(models.Model) :
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    detail_text = models.CharField(max_length=500)

    class Meta :
        db_table = 'ingredients'