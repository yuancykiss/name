from django.conf.urls import url

from xsdq import views

urlpatterns = [
    url(r'index/', views.Index.as_view()),
    url(r'search/', views.Search.as_view()),
    url(r'info/', views.Info.as_view()),
]