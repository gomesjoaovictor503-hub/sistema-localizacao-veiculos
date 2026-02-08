from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_carros, name='lista_carros'),
]