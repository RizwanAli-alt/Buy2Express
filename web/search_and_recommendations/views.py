from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from product_management.models import Product
from .models import SearchQuery, Recommendation
from .forms import SearchQueryForm

def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
          
            if request.user.is_authenticated:
                SearchQuery.objects.create(user=request.user, query=query)
           
            search_results = Product.objects.filter(name__icontains=query)
            return render(
                request, 
                'search_and_recommendations/search_results.html', 
                {'results': search_results, 'query': query}
            )
    return render(request, 'search_and_recommendations/search.html')

@login_required
def recommendations_view(request):
   
    recommendations = Recommendation.objects.filter(user=request.user).select_related('product')[:10]
    return render(
        request, 
        'search_and_recommendations/recommendations.html', 
        {'recommendations': recommendations}
    )
