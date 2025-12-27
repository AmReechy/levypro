from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import date
from django.core.mail import send_mail

from .models import Payment
from .receipt import Receipt
from levies.models import LevyType

from django.views.decorators.http import require_http_methods
from django.contrib import messages




@login_required
def make_payment(request):
    if request.method != "POST":
        return redirect("dashboard")

    outstanding_id = request.POST.get("outstanding_id")
    year, month, levy_name = outstanding_id.split("|")
    method = request.POST.get("method")

    levy = get_object_or_404(LevyType, name=levy_name)

    payment = Payment.objects.create(
        user=request.user,
        levy=levy,
        amount=levy.monthly_amount,
        method=method,
        month=date(int(year), int(month), 1),
        verified=True
    )

    receipt = Receipt.objects.create(payment=payment)
    receipt.generate()
    receipt.save()

    send_mail(
        subject="AMAC Levy Payment Confirmation",
        message=(
            f"Dear {payment.user.full_name},\n\n"
            f"Your payment of ₦{payment.amount} for {payment.levy.name} "
            f"has been received.\n\n"
            f"Reference: {payment.reference}\n\n"
            f"Please present your QR receipt for verification."
        ),
        from_email="no-reply@amac.gov.ng",
        recipient_list=[payment.user.email],
        fail_silently=True,
    )

    messages.success(request, f"Your payment of ₦{levy.monthly_amount} for {payment.month.strftime('%B %Y')} {levy.name} was successful.")

    return redirect("view_receipt", receipt_id=receipt.id)


@login_required
def view_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id, payment__user=request.user)
    return render(request, "receipt.html", {"receipt": receipt})


@require_http_methods(["GET", "POST"])
def verify_qr(request):
    result = None

    if request.method == "POST":
        reference = request.POST.get("reference")

        try:
            payment = Payment.objects.get(reference=reference)
            result = {
                "status": "VALID",
                "payment": payment
            }
        except Payment.DoesNotExist:
            result = {
                "status": "INVALID"
            }

    return render(request, "payments/verify_qr.html", {"result": result})
