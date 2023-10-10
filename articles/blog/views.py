from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    return HttpResponse("Blog app's page")

def categories(request, cat_id):
    return HttpResponse(f"<h1>Categories</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
    if request.POST:
         print(request.POST)
    return HttpResponse(f"<h1>Categories</h1><p>slug: {cat_slug}</p>")

def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('books', ))
        return redirect(uri)
    
    return HttpResponse(f"<h1>Archive</h1><p>year: {year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
