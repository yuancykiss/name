from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from xsdq.models import Surname, Name


class Index(APIView):

    # def get(self, request):
    #     surnames = Surname.objects.all()
    #     print(surnames)
    #     return render(request, 'index.html', {'surnames': surnames})

    def get(self, request):
        list1 = Surname.objects.all()
        paginator = Paginator(list1, 40)
        try:
            page = int(request.GET.get('page'))
        except:
            page = int(1)
        list = paginator.page(page)
        return render(request, 'index.html', {"list": list})


class Search(APIView):

    def get(self, request):
        surname = request.GET.get('surname')
        list1 = Name.objects.filter(name__startswith=surname)
        paginator = Paginator(list1, 40)
        try:
            page = int(request.GET.get('page'))
        except:
            page = int(1)
        list = paginator.page(page)
        return render(request, 'names.html', {"list": list, 'this_surname': surname})


class Info(APIView):

    def get(self, request):
        name = request.GET.get('name')
        this_name = Name.objects.filter(name=name)[0]
        if this_name.sex_boy > this_name.sex_girl:
            sex = 'boy'
        else:
            sex = 'girl'
        return render(request, 'info.html', {'this_name': this_name, 'sex': sex})
