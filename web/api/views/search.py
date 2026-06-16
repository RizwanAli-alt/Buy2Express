"""Search & Recommendations API with Elasticsearch."""
from elasticsearch_dsl import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from search_and_recommendations.documents import ProductDocument
from search_and_recommendations.models import Recommendation, SearchQuery
from ..serializers.products import ProductListSerializer
from ..serializers.search import RecommendationSerializer
from ..utils import StandardPagination


class SearchView(APIView):
    """
    GET /api/v1/search/?q=laptop&category=1&brand=2&min_price=100&max_price=500&sort=price_asc

    Full-text search with facets and sorting.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query     = request.query_params.get('q', '').strip()
        category  = request.query_params.get('category')
        brand     = request.query_params.get('brand')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        sort_by   = request.query_params.get('sort', 'relevance')

        if not query:
            return Response(
                {'detail': 'Query parameter `q` is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.is_authenticated:
            SearchQuery.objects.create(user=request.user, query=query)

        # ── Full-text query ───────────────────────────────────────────────
        search = ProductDocument.search().filter('term', is_active=True)
        search = search.query(
            Q('multi_match',
              query=query,
              fields=['name^3', 'description', 'category.name^2', 'brand.name^2'],
              fuzziness='AUTO')
        )

        # ── Filters ───────────────────────────────────────────────────────
        if category:
            search = search.filter('term', **{'category.id': int(category)})
        if brand:
            search = search.filter('term', **{'brand.id': int(brand)})
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

        # ── Facet aggregations ────────────────────────────────────────────
        search.aggs.bucket('categories',   'terms', field='category.name.keyword', size=20)
        search.aggs.bucket('brands',       'terms', field='brand.name.keyword',    size=20)
        search.aggs.bucket('price_ranges', 'range', field='price', ranges=[
            {'key': 'Under $25',   'to':   25},
            {'key': '$25 - $50',   'from': 25,  'to': 50},
            {'key': '$50 - $100',  'from': 50,  'to': 100},
            {'key': '$100 - $200', 'from': 100, 'to': 200},
            {'key': 'Over $200',   'from': 200},
        ])

        # ── Paginate ──────────────────────────────────────────────────────
        page      = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start     = (page - 1) * page_size
        response  = search[start:start + page_size].execute()

        results = [{
            'id':          hit.id,
            'name':        hit.name,
            'price':       hit.price,
            'category':    hit.category.name if hasattr(hit, 'category') else '',
            'brand':       hit.brand.name    if hasattr(hit, 'brand')    else '',
            'score':       hit.meta.score,
        } for hit in response]

        facets = {
            'categories':   [{'name': b.key, 'count': b.doc_count}
                             for b in response.aggregations.categories.buckets],
            'brands':       [{'name': b.key, 'count': b.doc_count}
                             for b in response.aggregations.brands.buckets],
            'price_ranges': [{'name': b.key, 'count': b.doc_count}
                             for b in response.aggregations.price_ranges.buckets],
        }

        return Response({
            'count':   response.hits.total.value,
            'page':    page,
            'results': results,
            'facets':  facets,
        })


class AutocompleteView(APIView):
    """
    GET /api/v1/search/autocomplete/?q=lap
    Returns up to 8 typeahead suggestions.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if len(query) < 2:
            return Response({'suggestions': []})

        search = ProductDocument.search().filter('term', is_active=True)
        search = search.query(
            Q('multi_match',
              query=query,
              fields=['name^3', 'category.name', 'brand.name'],
              type='phrase_prefix')
        )[:8]

        suggestions = [{'id': hit.id, 'name': hit.name, 'price': hit.price}
                       for hit in search.execute()]

        return Response({'suggestions': suggestions})


class RecommendationsView(APIView):
    """
    GET /api/v1/recommendations/
    Returns up to 10 personalised recommendations.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recs = Recommendation.objects.filter(
            user=request.user
        ).select_related('product')[:10]
        return Response(
            RecommendationSerializer(recs, many=True, context={'request': request}).data
        )