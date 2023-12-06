from django.shortcuts import get_object_or_404
from django.conf import settings
import stripe

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_item_session_id(request, pk):
    item = get_object_or_404(Item, id=pk)

    session = stripe.checkout.Session.create(
        # payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success'),
        cancel_url=request.build_absolute_uri(item.get_absolute_url()),
    )
    return session


def get_order_session_id(request, pk):
    """ Получение stripeID для заказа нескольких продуктов"""
    order = get_object_or_404(Order, id=pk)

    session = stripe.checkout.Session.create(
        # payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            } for item in order.items.all()
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/success'),
        cancel_url=request.build_absolute_uri(order.get_absolute_url()),
    )
    return session
