from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Burger(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderburgers = OrderBurger.objects.filter(order=self.id)
        for i in orderburgers:
            if i.burger.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderburgers = OrderBurger.objects.filter(order=self.id)
        total = sum([burger.get_total for burger in orderburgers])
        return total

    @property
    def get_cart_burgers(self):
        orderburgers = OrderBurger.objects.filter(order=self.id)
        total = sum([burger.quantity for burger in orderburgers])
        return total


class OrderBurger(models.Model):
    burger = models.ForeignKey(
        Burger, related_name='burger', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(
        Order, related_name='order', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.burger.price * self.quantity
        return total

    @property
    def get_burger(self):
        return self.burger.name

    @property
    def get_customer(self):
        return self.order.customer.name


class Address(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
