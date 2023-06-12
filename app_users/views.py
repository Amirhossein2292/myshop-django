from django.contrib.auth import get_user_model, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework import permissions, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = serializer.save()
            if user:
                refresh = RefreshToken.for_user(user)

                response = Response(
                    {
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                    },
                    status=status.HTTP_201_CREATED,
                )

                # Set the access token as an HTTP-only cookie
                access_token = str(refresh.access_token)
                response.set_cookie("access_token", access_token, httponly=True)

                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Set the access token as an HTTP-only cookie
        access_token = response.data.get("access")
        response.set_cookie("access_token", access_token, httponly=True)

        return response


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        # Delete the access token cookie
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        return response


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
