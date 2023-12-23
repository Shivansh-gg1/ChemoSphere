from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import login, authenticate, logout



class userViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class registerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        Serializer = self.get_serializer(data=request.data)
        Serializer.is_valid(raise_exception=True)
        self.perform_create(Serializer)
        user = Serializer.save()

        user.set_password(request.data['password'])
        user.is_logged = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        token = Token.objects.get_or_create(user=user)[0].key
        responseData = {
            "detail": {
                "message": "User successfully registered",
                "email": Serializer.data['email'],
                "first_name": Serializer.data['first_name'],
                "last_name": Serializer.data['last_name']
            }
        }
        responseData['detail'].update(token)
        headers = self.get_success_headers(Serializer.data)
        return Response(responseData, status=200, headers=headers)


class loginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = authenticate(
            request, email=request.data['email'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get_or_create(user=user)[0].key
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user.is_logged = True
            user.save()
            response = {
                "detail": {
                    "message": "User successfully logged in",
                    "email": user.email,
                    "is_email_verified": user.is_email_verified
                }
            }
            return Response(response, status=200)
        else:
            return Response({"detail": "Incorrect credentials"}, status=400)


class logoutViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )

    queryset = User.objects.all()
    serializer_class = UserSerializer
    def list(self, request, *args, **kwargs):

        Token.objects.filter(user=request.user).delete()
        request.user.is_logged = False
        request.user.save()
        logout(request)
        return Response({"detail": "user successfully logged out"}, status=200)
