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
    path('equipments/', views.equipment, name = 'dashboard-equipments'),
    path('equipments/edit/<int:pk>/', views.equipment_edit, name='dashboard-equipment-edit'),
    path('equipments/delete/<int:pk>/', views.equipment_delete, name='dashboard-equipment-delete'),
    path('equipments/view/<int:pk>/', views.equipment_view, name='dashboard-equipment-view'),
    path('product_csv', views.product_csv, name='product_csv'),
]