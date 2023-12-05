from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="login"),  # namespace 'users:login'
    path("logout/", LogoutView.as_view(), name="logout"),  # namespace 'users:logut'
    path("register/", views.RegisterUser.as_view(), name="register"),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]
