from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

from django.views.generic import RedirectView

urlpatterns = [
    # JWT token-related endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Existing URL patterns
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("user/", views.UserView.as_view(), name="user"),
    # Redirect root path to a specific URL
    path("", RedirectView.as_view(url="/api/")),
]
