import json
import bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View
from users.models           import User
from django.core.exceptions import ValidationError
from cores.validation       import validate_email, validate_password
from posea.settings         import SECRET_KEY, ALGORITHM

class CheckView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            email = data['email']

            validate_email(email)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : "LOGIN"}, status=200)

            return JsonResponse({'message' : "SIGNUP"}, status=200)
        
        except ValidationError as err:
            return JsonResponse({'message' : err.messages}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            
            email    = data['email']
            password = data['password']

            validate_email(email)
            validate_password(password)

            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email      = data['email'],
                password   = hashed_password,
                first_name = data['first_name'],
                last_name  = data['last_name']
            )
            return JsonResponse({"message": "SIGNUP_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except ValidationError as err:
            return JsonResponse({"message": err.messages}, status=400)


class LogInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            password = data['password']
            email    = data["email"]
            
            user     = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'token': token, 'first_name': user.first_name,  "last_name": user.last_name}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)