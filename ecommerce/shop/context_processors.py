from shop.models import Categories


def menu_links(request):
    c=Categories.objects.all()
    return {'links':c}   # we can use this data globally across all webpages inside our app
