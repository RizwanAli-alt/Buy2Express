from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from elasticsearch_dsl import Q
from product_management.models import Product
from .models import SearchQuery, Recommendation
from .documents import ProductDocument


def search_view(request):
    query        = request.GET.get('q', '').strip()
    category_id  = request.GET.get('category')
    brand_id     = request.GET.get('brand')
    min_price    = request.GET.get('min_price')
    max_price    = request.GET.get('max_price')
    min_rating   = request.GET.get('min_rating')
    sort_by      = request.GET.get('sort', 'relevance')

    results  = []
    facets   = {}
    total    = 0

    if query:
        # Log search query for authenticated users
        if request.user.is_authenticated:
            SearchQuery.objects.create(user=request.user, query=query)

        # ── Build full-text query ─────────────────────────────────────────
        search = ProductDocument.search().filter('term', is_active=True)

        search = search.query(
            Q('multi_match',
              query=query,
              fields=['name^3', 'description^1', 'category.name^2', 'brand.name^2'],
              fuzziness='AUTO',
              type='best_fields')
        )

        # ── Faceted filters ───────────────────────────────────────────────
        if category_id:
            search = search.filter('term', **{'category.id': int(category_id)})
        if brand_id:
            search = search.filter('term', **{'brand.id': int(brand_id)})
        if min_price:
            search = search.filter('range', price={'gte': float(min_price)})
        if max_price:
            search = search.filter('range', price={'lte': float(max_price)})

        # ── Sorting ───────────────────────────────────────────────────────
        sort_map = {
            'price_asc':  'price',
            'price_desc': '-price',
            'name':       'name.keyword',
            'relevance':  '_score',
        }
        search = search.sort(sort_map.get(sort_by, '_score'))

        # ── Aggregations (facets) ─────────────────────────────────────────
        search.aggs.bucket('categories', 'terms', field='category.name.keyword', size=20)
        search.aggs.bucket('brands',     'terms', field='brand.name.keyword',    size=20)
        search.aggs.bucket('price_ranges', 'range', field='price', ranges=[
            {'key': 'Under $25',    'to':   25},
            {'key': '$25 - $50',    'from': 25,  'to': 50},
            {'key': '$50 - $100',   'from': 50,  'to': 100},
            {'key': '$100 - $200',  'from': 100, 'to': 200},
            {'key': 'Over $200',    'from': 200},
        ])

        response = search[:50].execute()
        total    = response.hits.total.value

        # bulk-fetch slugs in one query to avoid N+1 lookups
        hit_ids  = [hit.id for hit in response]
        slug_map = dict(Product.objects.filter(pk__in=hit_ids).values_list('id', 'slug'))

        results = [{
            'id':          hit.id,
            'name':        hit.name,
            'description': hit.description,
            'price':       hit.price,
            'slug':        slug_map.get(int(hit.id), ''),
            'category':    hit.category.name if hasattr(hit, 'category') else '',
            'brand':       hit.brand.name    if hasattr(hit, 'brand')    else '',
            'score':       hit.meta.score,
        } for hit in response]

        # ── Build facets for template ─────────────────────────────────────
        facets = {
            'categories':  [{'name': b.key, 'count': b.doc_count}
                            for b in response.aggregations.categories.buckets],
            'brands':      [{'name': b.key, 'count': b.doc_count}
                            for b in response.aggregations.brands.buckets],
            'price_ranges':[{'name': b.key, 'count': b.doc_count}
                            for b in response.aggregations.price_ranges.buckets],
        }

    return render(request, 'search_and_recommendations/search_results.html', {
        'results':  results,
        'query':    query,
        'facets':   facets,
        'total':    total,
        'filters': {
            'category_id': category_id,
            'brand_id':    brand_id,
            'min_price':   min_price,
            'max_price':   max_price,
            'sort_by':     sort_by,
        }
    })


def autocomplete_view(request):
    """
    GET /search/autocomplete/?q=lap
    Returns up to 8 product name suggestions as JSON.
    """
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    search = ProductDocument.search().filter('term', is_active=True)
    search = search.query(
        Q('multi_match',
          query=query,
          fields=['name^3', 'category.name^2', 'brand.name'],
          type='phrase_prefix')
    )[:8]

    suggestions = [{'id': hit.id, 'name': hit.name, 'price': hit.price}
                   for hit in search.execute()]

    return JsonResponse({'suggestions': suggestions})


@login_required
def recommendations_view(request):
    recommendations = Recommendation.objects.filter(
        user=request.user
    ).select_related('product')[:10]
    return render(request, 'search_and_recommendations/recommendations.html', {
        'recommendations': recommendations
    })