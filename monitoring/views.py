from django.shortcuts import render
from payments.models import Payment

def dashboard(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"payments": payments})

