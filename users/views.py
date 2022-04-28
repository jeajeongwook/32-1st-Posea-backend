import json
from unicodedata import name
import bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View
from users.models           import User
from django.core.exceptions import ValidationError
from cores.validation       import email_validate, password_validate
from posea.settings         import SECRET_KEY,ALGORITHM




class CheckView(View):
    def post(self, request):
        data      = json.loads(request.body)
        try:
        
            email = data['email']

            email_validate(email)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : "Go_To_LogIn"}, status=200)

            return JsonResponse({'message' : "Go_To_SignUp"}, status=200)
        
        except ValidationError as err:
            return JsonResponse({'message' : err.messages}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


class SignUpView(View):
    def post(self, request):
        data      = json.loads(request.body)
        hashed_password     = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')

        try:

            email           = data['email']
            password        = data['password']

            email_validate(email)
            password_validate(password)

            User.objects.create(
                email           = data['email'],
                password        = hashed_password,
                first_name      = data['first_name'],
                last_name       = data['last_name']
            )
            return JsonResponse({"message": "SIGNUP_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except ValidationError as err:
            return JsonResponse({"message": err.messages}, status=400)


class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            password        = data['password']
            email           = data["email"]
            
            user     = User.objects.get(email=email)
            token    = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)

            if not bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            return JsonResponse({'message':'LOGIN_SUCCESS', 'token':token, 'first_name':user.first_name,  "last_name":user.last_name}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)