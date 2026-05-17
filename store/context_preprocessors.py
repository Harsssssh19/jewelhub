from django.core.cache import cache

from .models import Category, Cart


CART_COUNT_SESSION_KEY = 'store_cart_count'


def get_cart_count_for_request(request):
    if not request.user.is_authenticated:
        return 0

    cached_count = request.session.get(CART_COUNT_SESSION_KEY)
    if cached_count is not None:
        return int(cached_count)

    cart_count = Cart.objects.filter(user=request.user).count()
    request.session[CART_COUNT_SESSION_KEY] = cart_count
    request.session.modified = True
    return cart_count


def set_cart_count_for_request(request, cart_count):
    request.session[CART_COUNT_SESSION_KEY] = max(int(cart_count), 0)
    request.session.modified = True


def clear_cart_count_for_request(request):
    request.session.pop(CART_COUNT_SESSION_KEY, None)
    request.session.modified = True


def store_menu(request):
    categories = cache.get_or_set(
        'store_menu_categories_v1',
        list(Category.objects.filter(is_active=True).values('title', 'slug').order_by('title')),
        300,
    )
    context = {
        'categories_menu': categories,
    }
    return context

def cart_menu(request):
    if request.user.is_authenticated:
        cart_count = get_cart_count_for_request(request)
        context = {
            'cart_count': cart_count,
        }
    else:
        context = {}
    return context