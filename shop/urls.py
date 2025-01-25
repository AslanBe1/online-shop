from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='apelsin'),
    path('product_about/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/',views.about,name='about'),
    path('category-choice/<int:category_id>/', views.index, name='category_detail'),
    path('order-save-detail<int:pk>/save/', views.order_detail, name='order_detail'),
    path('comment-save-detail<int:pk>/save/', views.comment_detail, name='comment_detail'),
]