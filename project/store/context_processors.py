from .models import CartItem,Cart

def cart_item_count(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.filter(cart__customer=request.user, is_active=True)
            cart_item_count = sum(item.quantity for item in cart_items)


        except:
            pass
    return {'cart_item_count': cart_item_count}