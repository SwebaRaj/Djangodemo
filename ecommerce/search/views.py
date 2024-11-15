from django.shortcuts import render
from shop.models import product
from django.db.models import Q


def search_products(request):
    p = None
    query = ""
    if(request.method=="POST"):
        query=request.POST.get('q')
        if query:
            p=product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))     #filter the record matching with query
    context={'pro':p,'query':query}
    return render(request,'search.html',context)
