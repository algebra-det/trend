from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, ProductCategory, ProductRequest
from .forms import ProductForm, ProductCategoryForm, ProductFullfillForm

from django.views.generic import ListView, DetailView
from trend.mixins import UserIsAdmin

from trend.decorators import admin_only
from trend.mixins import UserIsAdmin

# Product
class ProductListView(UserIsAdmin, ListView):
    model = Product
    context_object_name = 'products'
    ordering = ('-points')
    template_name = 'product/products.html'



class ProductDetailView(UserIsAdmin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product_details.html'


@admin_only
def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print('**************************8')
        print('got POost')
        if form.is_valid():
            print('form is valid')
            form.save()
            print('form is saved')
            title = form.cleaned_data.get('title')
            messages.success(request, f"{title} è stato aggiunto con successo!")
            return redirect('product:index')
    form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'product/create_product.html', context)


@admin_only
def edit(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f'{title} è stato modificato con successo !')
            return redirect('product:index')
        else:
            messages.error(request, 'Qualcosa è andato storto' )
    
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form
    }
    return render(request, 'product/edit_product.html', context)


# Delete Product
@admin_only
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        Product.objects.filter(pk=id).delete()
        messages.success(request, f'Prodotto eliminato con successo!')
        return redirect('product:index')
    context = {
        'product': product
    }
    return render(request, 'product/delete_product.html', context)



# Categories
@admin_only
def category(request):
    categories = ProductCategory.objects.all()
    context = {'categories': categories}
    return render(request, 'product/product_category.html', context)



@admin_only
def add_category(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f"{title} è stato aggiunto con successo!")
            return redirect('product:category')

    # categories = ProductCategory.objects.all()
    form = ProductCategoryForm()
    context = {
        'form': form,
        # 'categories': categories
    }
    return render(request, 'product/create_product_category.html', context)


@admin_only
def edit_category(request, id):
    category = get_object_or_404(ProductCategory, pk=id)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"La categoria è stata aggiornata con successo!")
            return redirect('product:category')

    else:
        form = ProductCategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'product/edit_product_category.html', context)


# Delete Product
@admin_only
def delete_category(request, id):
    category = get_object_or_404(ProductCategory, pk=id)
    products = Product.objects.filter(category=category).count()
    if request.method == 'POST':
        category.delete()
        messages.success(request, f"La categoria è stata eliminata con successo!")
        return redirect('product:index')
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'product/delete_category.html', context)




# Product Request
@admin_only
def product_request(request):
    product_requests = ProductRequest.objects.all().order_by('-created_at')
    context = {
        'product_requests': product_requests,
    }
    return render(request, 'product/product_requests.html', context)


@admin_only
def product_request_detail(request, id):
    product_request = get_object_or_404(ProductRequest, pk=id)
    context = {
        'product_request': product_request,
    }
    return render(request, 'product/product_request_detail.html', context)


@admin_only
def update(request, id):
    product_request = get_object_or_404(ProductRequest, pk=id)
    if request.POST:
        form = ProductFullfillForm(request.POST, instance=product_request)
        if form.is_valid():
            form.save()
            messages.success(request, f"La richiesta del prodotto è stata aggiornata correttamente!")
            return redirect('product:product_request')
    else:
        form = ProductFullfillForm(instance=product_request)

    context = {
        'product_request': product_request,
        'form': form
    }

    return render(request, 'product/edit_product_request.html', context)


@admin_only
def product_request_delete(request, id):
    product_request = get_object_or_404(ProductRequest, pk=id)
    if request.method == 'POST':
        product_request.delete()
        messages.success(request, f"La richiesta del prodotto è stata eliminata correttamente!")
        return redirect('product:product_request')
    context = {
        'product_request': product_request
    }
    return render(request, 'product/delete_product_request.html', context)
