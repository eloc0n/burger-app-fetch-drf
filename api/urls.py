from django.urls import path
from api import views

urlpatterns = [
    path('burger-list/', views.BurgerList.as_view()),
    path('order-list/', views.OrderList.as_view()),
    path('order-burger-list/', views.OrderBurgerList.as_view()),
    path('update-order-burger/<int:pk>/', views.UpdateOrder.as_view()),
    path('customer-list/', views.CustomerList.as_view()),
    path('update-list/', views.UpdateList.as_view()),
]
