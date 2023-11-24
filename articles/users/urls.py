from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login'),     # namespace 'users:login'
    path('logout/', views.logout_user, name='logout'),  # namespace 'users:logut'
]
