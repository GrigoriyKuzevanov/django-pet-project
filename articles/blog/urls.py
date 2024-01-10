from django.urls import path, re_path, register_converter

from blog import converters, views

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.PostHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="addpage"),
    path("contacts/", views.contacts, name="contacts"),
    path("login/", views.login, name="login"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", views.PostCategory.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", views.TagList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit"),
    path("delete/<slug:slug>/", views.DeletePage.as_view(), name="delete"),
    path("my_posts/", views.PostUser.as_view(), name="user_posts"),
]
