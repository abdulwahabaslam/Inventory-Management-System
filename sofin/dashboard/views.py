from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

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
    context = {
        'item':item,
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
def customer(request):
    return render(request, 'dashboard/customers.html')
