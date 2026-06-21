from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Brand, ProductImage, ProductSpecification, ProductVariant
from .forms import (
    ProductForm,
    CategoryForm,
    BrandForm,
    ProductImageForm,
    ProductSpecificationForm,
    ProductVariantForm,
    ProductImageFormSet
)
from django.db.models import Avg, Count
from reviews.models import Review

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


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand', 'seller'),
        slug=slug, is_active=True
    )
    variants = product.variants.all()
    images = product.images.all()
    specifications = product.specifications.all()
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    reviews = Review.objects.filter(product=product, is_approved=True).select_related('user').order_by('-created_at')
    rating_data = reviews.aggregate(avg=Avg('rating'), total=Count('id'))
    average_rating = round(rating_data['avg'] or 0, 1)
    review_count = rating_data['total']
    user_has_reviewed = (
        request.user.is_authenticated and
        Review.objects.filter(product=product, user=request.user).exists()
    )

    return render(request, 'product_management/product_detail.html', {
        'product': product, 'variants': variants, 'images': images,
        'specifications': specifications, 'related_products': related_products,
        'reviews': reviews[:5], 'review_count': review_count,
        'average_rating': average_rating, 'user_has_reviewed': user_has_reviewed,
    })


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect('product_management:products')
        # agar invalid hai to form/formset errors ke saath wapis render hoga
    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, 'product_management/product_form.html', {'form': form, 'formset': formset})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('product_management:products')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, 'product_management/product_form.html', {'form': form, 'formset': formset})


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
