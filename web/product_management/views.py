from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Brand, ProductImage, ProductSpecification, ProductVariant
from .forms import ProductForm, CategoryForm, BrandForm, ProductImageForm, ProductSpecificationForm, ProductVariantForm


def product_list(request):
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    brand_filter = request.GET.get('brand')
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_filter:
        products = products.filter(category__id=category_filter)
    if brand_filter:
        products = products.filter(brand__id=brand_filter)

    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'product_management/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'query': query,
        'category_filter': category_filter,
        'brand_filter': brand_filter
    })


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management:products')
    else:
        form = ProductForm()
    return render(request, 'product_management/product_form.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_management:products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_management/product_form.html', {'form': form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_management:products')
    return render(request, 'product_management/product_confirm_delete.html', {'product': product})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'product_management/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management:category_list')
    else:
        form = CategoryForm()
    return render(request, 'product_management/category_form.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('product_management:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'product_management/category_form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('product_management:category_list')
    return render(request, 'product_management/category_confirm_delete.html', {'category': category})


def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'product_management/brand_list.html', {'brands': brands})


def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management:brand_list')
    else:
        form = BrandForm()
    return render(request, 'product_management/brand_form.html', {'form': form})


def brand_update(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('product_management:brand_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'product_management/brand_form.html', {'form': form})


def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        brand.delete()
        return redirect('product_management:brand_list')
    return render(request, 'product_management/brand_confirm_delete.html', {'brand': brand})
