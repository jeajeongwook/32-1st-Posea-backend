import json
from os import name

from django.http      import JsonResponse
from django.views     import View
from products.models  import MainCategory, Category, Product

class MainView(View):
    def get(self, request):
        try:
            products = Product.objects.all()
            
            recommend_list = [{
                'id'             : product.id,
                'name'           : product.name,
                'product_images' : product.productimage_set.get().product_image_url,
                'skin_type'      : [skin.skin_type for skin in product.skins.all()]
            } for product in products]
            
            return JsonResponse({'result' : recommend_list}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'} , status = 401)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_EXIST'} , status = 401)

class ProductlistView(View):
    def get(self, request):
        try:
            main_category_id = request.GET.get('main_category_id', None)
            category_id      = request.GET.get('category_id', None)

            if main_category_id:
                categories = Category.objects.filter(main_category__id=main_category_id)

            if category_id:
                categories = Category.objects.filter(id=category_id)
            
            product_list = [{
                'main_category_id'   : category.main_category.id,
                'main_category_name' : category.main_category.name,
                'categories': {    
                    'category_id'             : category.id,
                    'category_name'           : category.name,
                    'category_description'    : category.main_description,
                    'category_subdescription' : category.sub_description
                },
                'products': [{
                    'id'             : product.id,
                    'product_name'   : product.name,
                    'product_price'  : [selection.price for selection in product.selection_set.all()],
                    'product_size'   : [selection.size for selection in product.selection_set.all()],
                    'product_images' : product.productimage_set.get().product_image_url
                }for product in category.product_set.all()]
            }for category in categories]
            return JsonResponse({'result' : product_list}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'} , status = 401)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_EXIST'} , status = 401)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            products = Product.objects.filter(id = product_id)

            product_detail = [{
                'id'              : product.id,
                'name'            : product.name,
                'texture'         : product.texture,
                'sense'           : product.sense,
                'detail'          : product.detail,
                'direction'       : product.direction,
                'usage'           : product.usage,
                'category_name'   : product.category.name,
                'price'           : [selection.price for selection in product.selection_set.all()],
                'size'            : [selection.size for selection in product.selection_set.all()],
                'product_images'  : product.productimage_set.get().product_image_url,
                'texture_images'  : product.productimage_set.get().texture_image_url,
                'skintype'        : [skin.skin_type for skin in product.skins.all()],
                'scent'           : [scent.name for scent in product.scents.all()],
                'ingredient_name' : product.ingredient_set.get().name,
                'detail_text'     : product.ingredient_set.get().detail_text
            } for product in products]

            return JsonResponse({"results": product_detail}, status=200) 

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_EXIST'}, status=401)
