from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='apelsin'),
    path('product_about/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('about/',views.about,name='about'),
    path('category-choice/<int:category_id>/', views.index, name='category_detail'),
    path('order-save-detail<int:pk>/save/', views.OrderCreateView.as_view(), name='order_detail'),
    path('comment-save-detail<int:pk>/save/', views.CommentCreateView.as_view(), name='comment_detail'),
    path('create-product', views.CreateProductView.as_view(), name='create_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:pk>/', views.EditProductView.as_view(), name='edit_product'),
]