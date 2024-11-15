"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
app_name='cart'
from cart import views

urlpatterns = [
    path('addtocar/<int:i>',views.addtocart,name="addtocart"),
    path('cart',views.cartview,name="cart"),
    path('cartremove/<int:i>',views.cartremove,name='cartremove'),
    path('delete/<int:i>',views.delete,name="delete"),
    path('order',views.order_form,name='order_form'),
    path('paymentstatus/<u>',views.paymentstatus,name="paymentstatus"),
    path('orderview',views.order_view,name='orderview'),
]

