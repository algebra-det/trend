from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from account.models import MyUser, Code
from core.models import Profile, Reward, UserGame, UserChallenge
from account.api.utils import get_code, sending_email, sending_code
import datetime

from django.contrib.auth import login as django_login, logout

from .serializers import AppleRegisterSerializer, LoginSerializer, RegisterSerializer, FacebookRegisterSerializer, ChangePasswordSerializer

from trend import utils


districts_dict = utils.get_districts_dict()


def check_expiration_code(time):
    code_created_time = time
    time_elapsed = datetime.datetime.now().timestamp() - code_created_time.timestamp()
    if time_elapsed > 1800:
        return False
    return True


class RegisterView(APIView):
    def post(self, request):
        email = request.data['email'].lower()
        if MyUser.objects.filter(email=email).exists():
            return Response({'status': False, 'Message': 'Questo indirizzo email esiste già'})
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print('User saved: ', user)
        welcome_points = Reward.objects.all().first().welcome
        Profile.objects.create(user=user, credits=welcome_points)

        profile = Profile.objects.get(user=user)
        print('Profile saved: ', profile)

        profile.latitude = districts_dict[user.province]['latitude']
        profile.longitude = districts_dict[user.province]['longitude']
        profile.save()


        usergame = UserGame.objects.create(profile=profile)
        usergame.save()

        random_code = get_code()
        Code.objects.create(user=user, confirmation_code=random_code, usage='Register')

        sending_code(random_code, user.email)

        return Response({'status': True, 'Message': 'Controlla la tua email per il codice di verifica!'})


class AppleRegisterAPIView(APIView):
    def post(self, request):
        try:
            login_type = request.data.get('login_type')
            apple_id = request.data.get('apple_id')
        except Exception as e:
            print(e)
            return Response({"error": "login_type & apple_id is required!"})

        email = request.data['email'].lower()

        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            if user.apple_id == apple_id:
                if user.last_login:
                    first_login = False
                else:
                    first_login = True

                token, created = Token.objects.get_or_create(user=user)
                if not created:
                    first_login = False
                user.last_login = datetime.datetime.now()
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({'status': True, "user_id": user.id, "token": token.key, 'first_login': first_login}, status=200)
            return Response({'status': False, 'Message': "Questo indirizzo email esiste già, L'ID di Facebook non corrisponde all'ID nel database per questa email"})

        serializer = AppleRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_verified = True
        user.save()
        welcome_points = Reward.objects.all().first().welcome
        Profile.objects.create(user=user, credits=welcome_points)

        profile = Profile.objects.get(user=user)
        if user.province:
            profile.latitude = districts_dict[user.province]['latitude']
            profile.longitude = districts_dict[user.province]['longitude']
            profile.save()

        usergame = UserGame.objects.create(profile=profile)
        usergame.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({'status': True, "user_id": user.id, "token": token.key}, status=200)


class FacebookRegisterView(APIView):
    def post(self, request):
        try:
            login_type = request.data.get('login_type')
            facebook_id = request.data.get('facebook_id')
        except Exception as e:
            return Response({"error": "login_type & facebook_id is required!"})
        email = request.data['email'].lower()
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            if user.facebook_id == facebook_id:
                if user.last_login:
                    first_login = False
                else:
                    first_login = True

                token, created = Token.objects.get_or_create(user=user)
                if not created:
                    first_login = False
                user.last_login = datetime.datetime.now()
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({'status': True, "user_id": user.id, "token": token.key, 'first_login': first_login}, status=200)
            return Response({'status': False, 'Message': "Questo indirizzo email esiste già, L'ID di Facebook non corrisponde all'ID nel database per questa email"})
        serializer = FacebookRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_verified = True
        user.save()
        welcome_points = Reward.objects.all().first().welcome
        Profile.objects.create(user=user, credits=welcome_points)

        profile = Profile.objects.get(user=user)
        if user.province:
            profile.latitude = districts_dict[user.province]['latitude']
            profile.longitude = districts_dict[user.province]['longitude']
            profile.save()

        usergame = UserGame.objects.create(profile=profile)
        usergame.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({'status': True, "user_id": user.id, "token": token.key}, status=200)


class GetVerifiedAPIView(APIView):
    def post(self, request):
        try:
            email = request.data['email'].lower()
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return Response({"error": "No User Found, Register if you are a new user!"})

        if user.is_verified == True:
            return Response({"error": "Account già verificato, puoi semplicemente accedere!"})
        else:
            if Code.objects.filter(user=user).exists():
                code = Code.objects.get(user=user)
                code.delete()
            random_code = get_code()
            Code.objects.create(user=user, confirmation_code=random_code, usage='Register')
            sending_code(random_code, user.email)
            return Response({"status": True, "message": "Controlla la tua email per il codice di verifica!"})

import datetime


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login:
            first_login = False
        else:
            first_login = True

        token, created = Token.objects.get_or_create(user=user)
        if not created:
            first_login = False
        user.last_login = datetime.datetime.now()
        user.save()
        return Response({'status': True, "user_id": user.id, "token": token.key, "first_login": first_login}, status=200)

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        # token.user.last_login = datetime.datetime.now()
        # token.user.save()
        # request.user.auth_token.delete()
        return Response({'status': True, 'Message': 'You have successfully logged out!'})


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data['email'].lower()
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return Response({"error": "No User Exist"})

        if not user.is_active:
            return Response({"error": "User is Not Active, Activate your account first!"})

        if Code.objects.filter(user=user).exists():
            if Code.objects.filter(user=user).first().usage == 'Register':
                return Response({"error": "Account is not Verified, Verify it first!"})
            Code.objects.get(user=user).delete()
        random_code = get_code()
        code = Code(user=user, confirmation_code=random_code, usage='Forgot')
        code.save()
        sending_code(random_code, user.email)
        return Response({"status": True, "msg": "Controlla la tua email per il codice di verifica!"})
        


class CodeVerificationAPIView(APIView):
    
    def post(self, request):
        try:
            code = request.data['code']
            user_code = Code.objects.get(confirmation_code=code)

            code_created_time = user_code.created_at
            if not check_expiration_code(code_created_time):
                user_code.delete()
                return Response({"error": "Code Expired, Request a New One!"})

            if user_code.usage == 'Register':
                user_code.user.is_verified = True
                user_code.user.save()
                user_code.delete()
                return Response({"status": True, "message": "L'account è stato verificato con successo"})
            return Response({"status": True, "code": code})
        except Code.DoesNotExist:
            return Response({"error": "Wrong Confirmation Code!"})

class NewPasswordAPIView(APIView):

    def post(self, request):
        try:
            code = request.data['code']
            user_code = Code.objects.get(confirmation_code=code)
        except Code.DoesNotExist:
            return Response({"error": "Wrong Confirmation Code!"})

        code_created_time = user_code.created_at
        if not check_expiration_code(code_created_time):
            user_code.delete()
            return Response({"error": "Codice scaduto, richiedine uno nuovo!"})

        try:
            password = request.data['password']
            confirm_password = request.data['confirm_password']
        except Exception as e:
            return Response({"error": "Both Fields are required!"})

        if password != confirm_password:
            return Response({"error": "Passwords do not match"})
        else:
            user = user_code.user
            user.set_password(password)
            user.save()
            user_code.delete()
            return Response({"status": True, "message": "la password è stata cambiata!"})


class UpdatePasswordAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        # if not user.check_password(serializer.validated_data['old_password']):
        #     return Response({"error": "Wrong old Password"}, status=400)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"status": True, "message": "Password aggiornata con successo!"})
        
