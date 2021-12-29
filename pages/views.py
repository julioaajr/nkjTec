from django.http import request
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

def Index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #meta = request.META
    #for key,value in meta.items():
    #    print(f'{key} -- {value}')
    return render(request, "pages/index.html")