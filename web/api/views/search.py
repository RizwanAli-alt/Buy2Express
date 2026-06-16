"""Search & Recommendations API."""
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from product_management.models import Product
from search_and_recommendations.models import Recommendation, SearchQuery
from ..serializers.products import ProductListSerializer
from ..serializers.search import RecommendationSerializer
from ..utils import StandardPagination


class SearchView(APIView):
    """
    GET /api/v1/search/?q=<query>&page=1&page_size=20

    Searches products by name & description.
    Logs the query if the user is authenticated.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'detail': 'Query parameter `q` is required.'}, status=400)

        if request.user.is_authenticated:
            SearchQuery.objects.create(user=request.user, query=query)

        products = Product.objects.filter(
            is_active=True
        ).filter(
            name__icontains=query
        ) | Product.objects.filter(
            is_active=True,
            description__icontains=query,
        )

        paginator = StandardPagination()
        page = paginator.paginate_queryset(products.distinct(), request)
        serializer = ProductListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class RecommendationsView(APIView):
    """
    GET /api/v1/recommendations/

    Returns up to 10 personalised product recommendations for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recs = (
            Recommendation.objects
            .filter(user=request.user)
            .select_related('product')[:10]
        )
        return Response(RecommendationSerializer(recs, many=True, context={'request': request}).data)