import json

from django.http      import JsonResponse
from django.views     import View
from products.models  import MainCategory, Category, Product

class MainView(View):
    def get(self, request):
        # 1. request에서 데이터를 꺼내주기 위해 get을 선언한다.
        # 2. products 테이블에서 전체 데이터를 Product.objects.all()을 통해 가져온다.
        # 3. For문을 통해 각 제품의 name, product_imges, skintype 데이터를 가져온다.
        # 4. for문을 통해 가져온 데이터를 append로 recommend_list에 모아준다.
        # 5. 성공적으로 가져왔을 경우 recommend_list를 전달한다.
        try:
            products = Product.objects.all()
            
            recommend_list = [
                {
                    'id'             : product.id,
                    'name'           : product.name,
                    'product_images' : product.productimage_set.get().product_image_url,
                    'skin_type'      : [skin.skin_type for skin in product.skins.all()]
                }for product in products]
            
            return JsonResponse({'result' : recommend_list}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'} , status = 401)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_EXIST'} , status = 401)

class ProductlistView(View):
        # 1. request에서 데이터를 꺼내주기 위해 get을 선언한다.
        # 2. if문+filter를 통해 접속한 경로에 따라 해당 상위 category_id, main_category_id에 속하는 데이터를 가져올 수 있게 세팅한다.
        # 3. 중복 For문을 통해 category와 product에서 필요한 데이터를 가져온다.
        # 4. 가져온 데이터를 append로 product_list에 모아준다.
        # 4. 성공적으로 가져왔을 경우 category_id, main_category_id에 맞는 product_list를 전달한다.
    def get(self, request):
        try:
            main_category_id = request.GET.get('main_category_id', None)
            category_id      = request.GET.get('category_id', None)
            name             = request.GET.get('search', None)

            if name:
                products = Product.objects.filter(name__icontains=name)

            if main_category_id:
                categories = Category.objects.filter(main_category__id=main_category_id)
                products = Product.objects.filter(category__main_category__id=main_category_id)

            if category_id:
                products = Product.objects.filter(category_id=category_id)            
                categories = Category.objects.filter(id=category_id)
            
            # categories = {}
            #     if product.category.name in categories:
            #         categories.append(product.category.name)
            #     else:
            #         
                
            product_list = [{
                    
                    'category_name'           : category.name,
                    'category_description'    : category.main_description,
                    'category_subdescription' : category.sub_description,
                    'product' :[{
                        'id'             : product.id,
                        'category_id'    : product.category.id,
                        'product_name'   : product.name,
                        'product_price'  : [selection.price for selection in product.selection_set.all()],
                        'product_size'   : [selection.size for selection in product.selection_set.all()],
                        'product_images' : product.productimage_set.get().product_image_url
                        }for product in products]
                }for category in categories]
            return JsonResponse({'result' : product_list}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'} , status = 401)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_EXIST'} , status = 401)


class ProductDetailView(View):
    def get(self, request, product_id):
        # 1. request에서 데이터를 꺼내주기 위해 get을 선언한다.
        # 2. products 테이블에서 Product.objects.filter(id = product_id)을 통해 해당되는 제품의 id에 맞는 데이터를 가져온다.
        # 3. For문을 통해 product에서 필요한 데이터를 가져온다.
        # 4. 가져온 데이터를 append로 product_detail에 모아준다.
        # 4. 성공적으로 가져왔을 경우 filter(id = product_id)에 맞는 product_detail을 전달한다.
        try:
            products = Product.objects.filter(id = product_id)

            product_detail = [
                {
                    'id'                : product.id,
                    'name'              : product.name,
                    'texture'           : product.texture,
                    'sense'             : product.sense,
                    'detail'            : product.detail,
                    'direction'         : product.direction,
                    'usage'             : product.usage,
                    'category_name'     : product.category.name,
                    'price'             : [selection.price for selection in product.selection_set.all()],
                    'size'              : [selection.size for selection in product.selection_set.all()],
                    'product_images'    : product.productimage_set.get().product_image_url,
                    'texture_images'    : product.productimage_set.get().texture_image_url,
                    'skintype'          : [skin.skin_type for skin in product.skins.all()],
                    'scent'             : [scent.name for scent in product.scents.all()],
                    'ingredient_name'   : product.ingredient_set.get().name,
                    'detail_text'       : product.ingredient_set.get().detail_text
                } for product in products]
            return JsonResponse({"results": product_detail}, status=200) 
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'} , status = 401)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_EXIST'} , status = 401)
