from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from .models import Item, Order
import stripe
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from . import services

# stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['GET'])
def get_checkout_session_id(request, pk):
    """ Получение stripeID для покупки продукта"""
    session = services.get_item_session_id(request, pk)
    return JsonResponse(session, status=200)


@require_GET
def item(request, pk):
    item = Item.objects.get(id=pk)
    return render(request,
                   "item.html",
                   {"item": item,
                    "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
                   }
                )


@api_view(['GET'])
def get_checkout_order_session_id(request, pk):
    """ Получение stripeID для заказа нескольких продуктов"""

    session = services.get_order_session_id(request, pk)
    return JsonResponse(session, status=200)


@require_GET
def get_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    items = order.items.all()
    total_price = sum(item.price for item in items)
    return render(request, 'order.html',
                  {'items': items,
                   'total_price': total_price,
                   'order': order,
                   "stripe_key": settings.STRIPE_PUBLISHABLE_KEY
                  }
                 )


class SuccessView(View):
    def get(self, request):
        return render(request, 'success.html', status=200)
