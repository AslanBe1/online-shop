from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='apelsin'),
    path('detail.html/', views.product_detail,name='detail'),
]
