from .models import *
from .utils import cookieCart, cartData
from .serializers import *
import json
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class BurgerList(APIView):
    def get(self, request, format=None):

        burgers = Burger.objects.all()
        serializer = BurgerSerializer(burgers, many=True)
        return Response(serializer.data)


class OrderList(APIView):
    def get(self, request, format=None):

        # data = cartData(request)
        # print(data)

        # cartBurgers = data['cartBurgers']
        # order = data['order']
        # burgers = data['burgers']
        # print(request.user.customer)
        if request.user.is_authenticated:
            customer = request.user.customer
            orders = Order.objects.filter(customer=customer)
            # orders = Order.objects.all()
            # print(orders)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        else:
            return Response('')


class OrderBurgerList(APIView):
    def get(self, request, format=None):

        # data = cartData(request)

        # cartBurgers = data['cartBurgers']
        # order = data['order']
        # burgers = data['burgers']
        if request.user.is_authenticated:
            customer = request.user.customer
            # print(customer)

            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            # print(order)

            orderBurgers = OrderBurger.objects.filter(order=order)
            print(customer, order, orderBurgers)

            serializer = OrderBurgerSerializer(orderBurgers, many=True)
            return Response(serializer.data)
        else:
            return Response('')

    def post(self, request, format=None):

        if request.user.is_authenticated:
            # if not Order.objects.exists():
            #     print('it exists dummy')
            #     serializer = OrderBurgerSerializer(data=request.data)
            # else:
            #     customer = request.user.customer
            #     order, created = Order.objects.get_or_create(
            #         customer=customer, complete=False)
            #     print('hello', customer, order)

            #     burgers = Burger.objects.get(id=1)
            #     print(burgers)

            #     data = {
            #         'burger': burgers.id,
            #         'quantity': 1,
            #         'order': order.id,
            #     }

            #     print(data)
            #     serializer = OrderBurgerSerializer(data=data)

            # cartBurgers = order.get_cart_burgers
            # print(cartBurgers)

            serializer = OrderBurgerSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateOrder(APIView):
    def get_burger(self, pk):
        try:
            return OrderBurger.objects.get(pk=pk)
        except OrderBurger.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order_burger = self.get_burger(pk)
        serializer = OrderBurgerSerializer(order_burger)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order_burger = self.get_burger(pk)
        serializer = OrderBurgerSerializer(order_burger, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order_burger = self.get_burger(pk)
        order_burger.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerList(APIView):
    def get(self, request, format=None):

        # data = cartData(request)

        # cartBurgers = data['cartBurgers']
        # order = data['order']
        # burgers = data['burgers']

        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class UpdateList(APIView):
    def post(self, request, format=None):
        # data = json.loads(request.body)
        # print(data)
        # productId = data['productId']
        # action = data['action']
        # print('Action:', action)
        # print('Product:', productId)
        # data = cartData(request)

        # cartBurgers = data['cartBurgers']
        # order = data['order']
        # burgers = data['burgers']

        # serializer = OrderSerializer(data=request.data)
        # if serializer.is_valid():
        #     # serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
