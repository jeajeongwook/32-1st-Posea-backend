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
        # 1. request에서 body를 가져온다.
        # 2. body에서 원하는 데이터를 꺼낸다.
        # 3. email 유효성 검사 진행
        # 4. if문으로 db에 email 있는지 확인
        # 5. 있으면 LOGIN 메세지 전달, 없으면 SIGNUP 메세지 전달

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
        # 1. request에서 body를 가져온다.
        # 2. body에서 원하는 데이터를 꺼낸다.
        # 3. email과 password에 대해 유효성 검사 진행
        # 4. password를 암호화 작업 진행한다.
        # 5. create로 데이터를 생성해서 db에 추가한다.
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
        # 1. request에서 body를 가져온다.
        # 2. body에서 원하는 데이터를 꺼낸다.
        # 3. user를 email로 정의한다.
        # 4. email과 암호화된 패스워드에 대해 if문으로 매칭여부를 확인한다.
        # 5. 정상적으로 매칭되는점 확인시 token을 부여한다.
        # 6. 결과를 리턴시 토큰과 이용자의 이름을 같이 넘겨준다.
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