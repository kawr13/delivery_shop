"""
URL configuration for delveryclub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import Startpage, BasketAdd, BasketView, BasketRemoveItemView, BasketRemoveView, BisnessMenuView, BasketAddItem,\
OrderView

app_name = 'startpage'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Startpage.as_view(), name='startpage'),
    path('add/<int:product_id>/', BasketAdd.as_view(), name='basket_add'),
    path('rem_item/<int:product_id>/', BasketRemoveItemView.as_view(), name='basket_rem_item'),
    path('add_item/<int:product_id>/', BasketAddItem.as_view(), name='basket_add_item'),
    path('rem/', BasketRemoveView.as_view(), name='basket_rem'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('bmenu/', BisnessMenuView.as_view(), name='bmenu'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:order_id>/', OrderView.as_view(), name='order'),
]

