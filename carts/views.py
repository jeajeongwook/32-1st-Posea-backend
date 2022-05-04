from itertools import count
import json

from django.http import JsonResponse
from django.views import View
from cores.utils import author
from carts.models import Cart

# Create your views here.

class CartView(View):
    @author
    def post(self, request):
        try:
            data = json.loads(request.body)

            Cart.objects.create(
                user       = request.user,
                product_id = data['product_id']
                
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_DOES_NOT_EXIT'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @author
    def get(self, request):
        try:
            user  = request.user
            carts = Cart.objects.filter(user=user)

            cart_list = [{
                'user_id'      : user.id,
                'cart_id'      : cart.id,
                'count'        : cart.count,
                'product_id'   : cart.product.id,
                'product_name' : cart.product.name,
                'product_size' : [selection.size for selection in cart.product.selection_set.all()],
                'totalPrice'   : int(cart.count * [selection.price for selection in cart.product.selection_set.all()])
            } for cart in carts]

            return JsonResponse({'result': cart_list}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_DOES_NOT_EXIT'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @author
    def delete(self, request):
        try:
            cart_ids = request.GET.getlist('cart_ids')
            user     = request.user

            Cart.objects.filter(id__in=cart_ids, user_id=user).delete()

            return JsonResponse({'message': 'CART_DELETED'}, status=200)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)