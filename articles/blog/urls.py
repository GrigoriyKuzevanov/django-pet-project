from django.urls import path, re_path, register_converter
from blog import views
from blog import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('addpage00/', views.addpage, name='addpage'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<int:cat_id>', views.show_category, name='category'),
]
