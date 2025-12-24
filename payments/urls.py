from django.urls import path
from .views import make_payment, view_receipt, verify_qr

#app_name = "payments"

urlpatterns = [
    path("pay/", make_payment, name="make_payment"),
    path("receipt/<int:receipt_id>/", view_receipt, name="view_receipt"),
    path("verify/", verify_qr, name="verify_qr"),
]
