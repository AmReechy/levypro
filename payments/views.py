from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Payment
from .receipt import Receipt
from django.core.mail import send_mail
from levies.models import LevyType

def make_payment(request):
    if request.method == "POST":
        levy_id = request.POST["levy"]
        method = request.POST["method"]

        levy = LevyType.objects.get(id=levy_id)

        payment = Payment.objects.create(
            user=request.user,
            levy=levy,
            amount=levy.monthly_amount,
            method=method,
            month=now().date()
        )

        receipt = Receipt.objects.create(payment=payment)
        receipt.generate()
        receipt.save()

        send_mail(
            "AMAC Levy Payment Confirmation",
            f"Payment received. Ref: {payment.reference}",
            "no-reply@amac.gov.ng",
            [request.user.email],
        )

        return redirect("dashboard")
