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

            cart, created  = Cart.objects.get_or_create(
                user       = request.user,
                product_id = data['product_id']
            )
            if not created and cart.count < 20:
                cart.count += 1
                cart.save()

                return JsonResponse({'message': 'SUCCESS'}, status=200)
            elif not created and cart.count > 19:
                return JsonResponse({'message': 'INVALID_COUNT'}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_DOES_NOT_EXIT'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @author
    def get(self, request):

        user  = request.user
        carts = Cart.objects.filter(user=user)

        if not carts.exists():
            return JsonResponse({'message': 'INVALID_USER'}, status=400)

        cart_list = [{
            'user_id'      : user.id,
            'cart_id'      : cart.id,
            'count'        : cart.count,
            'product_id'   : cart.product.id,
            'product_name' : cart.product.name,
            'product_size' : cart.product.selection.size,
            'totalPrice'   : int(cart.count * cart.product.selection.price)
        } for cart in carts]
        return JsonResponse({'result': cart_list}, status=200)

    @author
    def patch(self, request, cart_id):
        try:
            data = json.loads(request.body)

            if data['count'] <= 0 or data['count'] >= 21:
                return JsonResponse({'message': 'INVALID_COUNT'}, status=400)

            if Cart.objects.filter(id=cart_id).exists():
                cart = Cart.objects.get(id=cart_id, user=request.user
                )
                cart.count = data['count']
                cart.save()
                return JsonResponse({'message': 'COUNT_CHANGED'}, status=201)

            return JsonResponse({'message': 'CART_DOES_NOT_EXIT'}, status=404)

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