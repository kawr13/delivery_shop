from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .geocheack import start
from .forms import *
from .models import *
import uuid
from icecream import ic


class Startpage(View):

    def get(self, request: HttpResponse):
        print('trolololo')
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            if not device:
                device = request.session.session_key or str(uuid.uuid4())
                print(device)

            try:
                user = User.objects.get(device=device)
            except User.DoesNotExist:
                user = User.objects.create(device=device)

        basket_quantity = Basket.objects.filter(user=user).total_quantity()
        product = Product.objects.all()[:10]
        context = {
            'title': 'Главная',
            'product': product,
            'basket_quantity': basket_quantity,
        }

        # Если заголовок X-Requested-With указывает на AJAX-запрос, возвращаем JSON
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            response_data = {
                'basket_quantity': basket_quantity,
                # Другие данные, если необходимо
            }
            return JsonResponse(response_data)

            # В противном случае возвращать HTML-страницу
        return render(request, 'startpage/page1.html', context=context)

class BasketAdd(View):

    @csrf_exempt
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            user, created = User.objects.get_or_create(device=device)
        baskets = Basket.objects.filter(user=user, product=product)
        if not baskets.exists():
            Basket.objects.create(user=user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()

        bask_quantity = Basket.objects.filter(user=user).total_quantity()

        return JsonResponse({'bask_quantity': bask_quantity})


class BasketView(View):

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            user, created = User.objects.get_or_create(device=device)
        baskets = Basket.objects.filter(user=user)
        context = {
            'title': 'Корзина',
            'baskets': baskets,
        }
        return render(request, 'startpage/basket.html', context=context)


class BasketRemoveItemView(View):

    def get(self, request, product_id):

        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            user, _ = User.objects.get_or_create(device=device)

        basket = Basket.objects.filter(user=user, product=product).first()

        if basket.quantity >= 1:
            basket.quantity -= 1
            if basket.quantity == 0:
                basket.delete()
            else:
                basket.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketAddItem(View):

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            user, created = User.objects.get_or_create(device=device)
        baskets = Basket.objects.filter(user=user, product=product)
        if not baskets.exists():
            Basket.objects.create(user=user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketRemoveView(View):

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            user, _ = User.objects.get_or_create(device=device)

        baskets = Basket.objects.filter(user=user)
        for basket in baskets:
            basket.delete()
        return HttpResponseRedirect(reverse('startpage:startpage'))


class BisnessMenuView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            user, _ = User.objects.get_or_create(device=device)
        product = Product.objects.all()
        baskets = Basket.objects.filter(user=user)
        context = {
            'title': 'Бизнес меню',
            'product': product,
            'baskets': baskets,
        }
        return render(request, 'startpage/bisneslaunch.html', context=context)


class OrderView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES.get('device')
            if not device:
                device = request.session.session_key or str(uuid.uuid4())
                print(device)

            try:
                user = User.objects.get(device=device)
            except User.DoesNotExist:
                user = User.objects.create(device=device)
        baskets = Basket.objects.filter(user=user)
        order = Order.objects.filter(user=user).first()
        total_sum = baskets.total_sum()

        if not order:
            order = Order.objects.create(user=user, quantity=1, total_sum=total_sum)
            for basket in baskets:
                basket.order = order
                basket.save()
        else:
            order.total_sum = total_sum
            order.save()
        context = {
            'title': 'Заказ',
            'order': order,
            'form': AdressForms(),
            'delivery': DeliveryOption.objects.filter(order=order).first(),
        }
        print(context)
        return render(request, 'startpage/order.html', context=context)

    def post(self, request, order_id):
        form = AdressForms(request.POST)
        if form.is_valid():
            adress = f"{form.cleaned_data['city']} {form.cleaned_data['street']} {form.cleaned_data['hause']}"
            dist_price = start(adress)

            order = get_object_or_404(Order, id=order_id)
            dely = DeliveryOption.objects.create(name=adress, price=dist_price)
            adress = Address.objects.create(orders=order, **form.cleaned_data)
            order.adress = adress
            order.delivery_option = dely
            order.save()
            return HttpResponseRedirect(reverse('startpage:orders'))
