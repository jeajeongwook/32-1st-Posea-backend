import json

from django.http     import JsonResponse
from django.views    import View
from products.models import Category, Product

class CategoryView(View):
    def get(self, request):
        categories  = Category.objects.all()
        products  = Product.objects.all()
        results = []
        for category in categories:
            for product in products:
                results.append(
                    {
                        "name"     : category.name,
                        'image'    : product.image.image_url,
                        'skintype' : types.skin_type.name,
                        "new"      : products.is_new
                    }
                )
        return JsonResponse({"results": results}, status=200)


class ProductView(View):
    def get(self, request):
        products  = Product.objects.all()
        results = []
        for product in products:
            results.append(
                {
                    "name"  : products.name,
                    "skin"  : products.product_skin.skin.skin_type,
                    "new"   : products.is_new,
                    "size"  : products.selections.size,
                    "price" : products.selections.price,
                    "usage" : products.usage
                }
            )
        return JsonResponse({"results": results}, status=200)


class ProductDetailView(View):
    def get(self, request):
        products  = Product.objects.all()
        results = []
        for product in products:
            results.append(
                {
                    "name"            : products.name,
                    "skin"            : products.product_skin.skin.skin_type,
                    "new"             : products.is_new,
                    "usage"           : products.usage,
                    "texture"         : products.texture,
                    "direction"       : products.direction,
                    "detail"          : products.detail,
                    "scent"           : products.product_scent.scents.name,
                    "Image"           : products.images.image_url,
                    "size"            : products.selections.size,
                    "price"           : products.selections.price,
                    "ingredient_name" : products.ingredients.ingredient_name,
                    "detail_text"     : products.ingredients.detail_text
                }
            )
