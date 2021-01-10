import json
from .models import *


def cookieCart(request):

    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    burgers = []
    order = {'get_cart_total': 0, 'get_cart_burgers': 0, 'shipping': False}
    cartBurgers = order['get_cart_burgers']

    for i in cart:
        # We use try block to prevent burgers in cart that may have been removed from causing error
        try:
            cartBurgers += cart[i]['quantity']

            burger = Burger.objects.get(id=i)
            total = (burger.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_burgers'] += cart[i]['quantity']

            burger = {
                'id': burger.id,
                'burger': {'id': burger.id, 'name': burger.name, 'price': burger.price,
                           'imageURL': burger.imageURL}, 'quantity': cart[i]['quantity'],
                'digital': burger.digital, 'get_total': total,
            }
            burgers.append(burger)

            if burger.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartBurgers': cartBurgers, 'order': order, 'burgers': burgers}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        print(customer)
        burgers = OrderBurger.objects.get(order=order)
        print(burgers)

        cartBurgers = order.get_cart_burgers
        print(cartBurgers)
    else:
        cookieData = cookieCart(request)
        cartBurgers = cookieData['cartBurgers']
        order = cookieData['order']
        burgers = cookieData['burgers']

    return {'cartBurgers': cartBurgers, 'order': order, 'burgers': burgers}
