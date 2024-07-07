from django.urls import path
from .views import (
    UserList, UserDetail,
    ProductCategoryList, ProductCategoryDetail,
    ProductList, ProductDetail,
    PetCategoryList, PetCategoryDetail,
    PetList, PetDetail,
    VaccinationList, VaccinationDetail,
    OrderList, OrderDetail,
    CommentList, CommentDetail,
    PostList, PostDetail,
    DoctorList, DoctorDetail,
    MessageList, MessageDetail,
)

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('product-categories/', ProductCategoryList.as_view(), name='product-category-list'),
    path('product-categories/<int:pk>/', ProductCategoryDetail.as_view(), name='product-category-detail'),

    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),

    path('pet-categories/', PetCategoryList.as_view(), name='pet-category-list'),
    path('pet-categories/<int:pk>/', PetCategoryDetail.as_view(), name='pet-category-detail'),

    path('pets/', PetList.as_view(), name='pet-list'),
    path('pets/<int:pk>/', PetDetail.as_view(), name='pet-detail'),

    path('vaccinations/', VaccinationList.as_view(), name='vaccination-list'),
    path('vaccinations/<int:pk>/', VaccinationDetail.as_view(), name='vaccination-detail'),

    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),

    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),

    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),

    path('doctors/', DoctorList.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),

    path('messages/', MessageList.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),
]
