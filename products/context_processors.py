from .models import Category


def navbar(request):
    categories = Category.objects.all()
    return {
        'categories': categories
    }
