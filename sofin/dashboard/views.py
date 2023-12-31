from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, InventoryMetrics, Equipment
from .forms import ProductForm, OrderForm, EquipmentForm
from django.contrib.auth.models import User
from django.contrib import messages
from joblib import load
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import csv

# Create your views here.

def product_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Deposition'] = 'attachment; filename=products.csv'

    #Creating a csv writer
    writer = csv.writer(response)

    #Designating the model
    products = Product.objects.all()

    #Adding Column headings to the csv file
    writer.writerow(['Product Name', 'Product Category', 'Quantity', 'Price Per Unit', 'Market Price', 'Cost of Goods Sold', 'Holding Cost', 'Obsolete Cost', 'Data Created'])

    for product in products:
        writer.writerow([product.name, product.category, product.quantity, product.cost_per_unit, product.market_price, product.cogs, product.holding_cost, product.obs_cost, product.created_at])

    return response


@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    items_count = products.count()
    workers_count = User.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders':orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'items_count': items_count,

    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    items_count = Product.objects.all().count()

    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'items_count': items_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    worker = User.objects.get(id=pk)
    context = {
        'worker': worker,
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required
def products(request):
    items = Product.objects.all() #ORM
    items_count = items.count()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-products')
    else:
        form = ProductForm()
    context = {
        'items': items,
        'form': form,
        'items_count': items_count,
        'workers_count': workers_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-products')
    return render(request, 'dashboard/products_delete.html')

@login_required
def product_view(request, pk):
    item = Product.objects.get(id=pk)
    try:
        inventory_metrics = InventoryMetrics.objects.get(product=item)
        turnover_rate = inventory_metrics.turnover_rate
    except InventoryMetrics.DoesNotExist:
        turnover_rate = 0
    
    # turnover_rate = 5.28
    holding_cost = item.holding_cost
    obsolescence_risk = item.obs_cost

    model = load('./Saved_Models/inventory_health_model.joblib')
    y_pred = model.predict([[turnover_rate, holding_cost, obsolescence_risk]])
    health = y_pred[0]

    context = {
        'item':item,
        'health': health,
    }
    return render(request, 'dashboard/product_view.html', context)

@login_required
def product_edit(request, pk):
    item = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            print('\nValid\n')
            form.save()
            return redirect('dashboard-products')
        else:
            print('Not Valid')
    else:
        form = ProductForm(instance=item)
        
    context = {
        'form': form,
    }
    return render(request, 'dashboard/products_edit.html', context)

@login_required
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count
    items_count = Product.objects.all().count
    context = {
        'orders': orders,
        'orders_count': orders_count,
        'workers_count': workers_count,
        'items_count': items_count,
    }
    return render(request, 'dashboard/order.html', context)

@login_required
def equipment(request):
    equipments = Equipment.objects.all()
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            equipment_name = form.cleaned_data.get('name')
            messages.success(request, f'{equipment_name} has been added')
            return redirect('dashboard-equipments')
    else:
        form = EquipmentForm()
    context = {
        'equipments': equipments,
        'form': form,
    }
    return render(request, 'dashboard/equipment.html', context)

@login_required
def equipment_delete(request, pk):
    equipment = Equipment.objects.get(id=pk)
    if request.method == 'POST':
        equipment.delete()
        return redirect('dashboard-equipments')
    context = {
        'equipment':equipment,
    }
    return render(request, 'dashboard/equipment_delete.html', context)

@login_required
def equipment_edit(request, pk):
    equipment = Equipment.objects.get(id=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('dashboard-equipments')
    else:
        form = EquipmentForm(instance=equipment)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/equipment_edit.html', context)

@login_required
def equipment_view(request, pk):
    equipment = Equipment.objects.get(id=pk)
    maintenance_required = equipment.is_maintenance_required()
    context = {
        'equipment':equipment,
        'maintenance_required': maintenance_required,
    }
    return render(request, 'dashboard/equipment_view.html', context)

@login_required
def customer(request):
    return render(request, 'dashboard/customers.html')
