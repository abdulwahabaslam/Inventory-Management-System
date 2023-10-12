from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'), 
    path('staff/detail/<int:pk>', views.staff_detail, name='dashboard-staff-detail'),
    path('products/', views.products, name='dashboard-products'),
    path('products/delete/<int:pk>/', views.product_delete, name='dashboard-products-delete'),
    path('products/edit/<int:pk>/', views.product_edit, name='dashboard-products-edit'),
    path('products/view/<int:pk>/', views.product_view, name='dashboard-product-view'),
    path('order/', views.order, name='dashboard-order'),
    path('customer/', views.customer, name='dashboard-customers'),
]