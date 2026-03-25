from django.urls import path

from .views import CreatePaymentView, PaymentListView

urlpatterns = [
    path("payments/", CreatePaymentView.as_view(), name="create-payment"),
    path("payments/list/", PaymentListView.as_view(), name="list-payments"),
]
