from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='apelsin'),
    path('product_about/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/',views.about,name='about'),
]
