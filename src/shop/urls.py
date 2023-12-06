from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:pk>/', views.get_checkout_session_id, name='get_checkout_session_id'),
    path('item/<int:pk>/', views.item, name='get_item'),
    path('success/', views.SuccessView.as_view()),
    path('order/<int:pk>', views.get_checkout_order_session_id, name='get_order'),
    path('buy/order/<int:pk>', views.get_order),
]
