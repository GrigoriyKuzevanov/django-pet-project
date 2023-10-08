from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Blog app's page")

def categories(request):
    return HttpResponse("<h1>Categories</h1>")
