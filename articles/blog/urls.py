from django.urls import path, re_path, register_converter
from blog import views
from blog import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.PostHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.PostCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagList.as_view(), name='tag'),
]
