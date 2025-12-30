
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import PayeeRegistrationForm
from .models import Payee
from payments.models import Payment
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib import messages

def register(request):
    form = PayeeRegistrationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        form.save_m2m()
        levy_types = form.cleaned_data["levy_types"]
        user.levy_types.set(levy_types)
        messages.success(request, "Your Payee Account was created successfully. You can now log in to the account with your credentials.")
        return redirect("login")
    #print(form.as_div())
    return render(request, "register.html", {"form": form})


def compute_outstanding_levies(payee):
    """
    Returns a list of outstanding levy obligations for a payee.
    Each item represents ONE levy for ONE unpaid month.
    """

    START_MONTH = date(2025, 1, 1)
    current_month = date.today().replace(day=1)

    # Generate all months from Jan 2025 to now
    all_months = []
    month_cursor = START_MONTH
    while month_cursor <= current_month:
        all_months.append(month_cursor)
        month_cursor += relativedelta(months=1)

    outstanding = []
    #print(list(map(lambda x:x.month, all_months)))

    # Loop through levy types applicable to the payee
    for levy in payee.levy_types.all():

        # Months already paid for this levy
        paid_months = set(
            Payment.objects.filter(
                user=payee,
                levy=levy,
                verified=True,
            ).values_list("month", flat=True)
        )

        # Any month not paid is outstanding
        for month in all_months:
            if month not in paid_months:
                outstanding.append({
                    "levy_id": levy.id,
                    "levy_name": levy.name,
                    "amount": levy.monthly_amount,
                    "month": month,
                    #"month": month.year,
                })

    return outstanding


def login_view(request):
    if request.method == "POST":
        id_number = request.POST["id_number"]
        phone = request.POST["phone"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=id_number,
            password=password,
            phone=phone
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid login credentials used!")

    return render(request, "login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("dashboard")



@login_required
def dashboard(request):
    payee=request.user
    outstanding_levies = compute_outstanding_levies(payee)
    payments = Payment.objects.filter(user=payee)
    #   print(1,2,3)
    context = {
        "outstanding_levies": outstanding_levies,
        "has_outstanding": bool(outstanding_levies),
        'payments':payments,
        # other context values you already have
    }
    return render(request, "dashboard.html", context)


@staff_member_required
def view_payee_info(request):
    payee_id = request.GET.get("id_number","")
    try:
        payee = Payee.objects.get(id_number=payee_id)
    except:
        if payee_id:
            messages.error(
                request,
                f"No payee found with ID number '{payee_id}'."
            )
        payee = None
    if payee:
        outstanding_levies = compute_outstanding_levies(payee)
        payments = Payment.objects.filter(user=payee)
    else:
        outstanding_levies = []
        payments = []
    context = {
        "outstanding_levies": outstanding_levies,
        "has_outstanding": bool(outstanding_levies),
        'payments':payments,
        "payee": payee,
        "searched_id": payee_id,
        # other context values you already have
    }
    return render(request, "payee_info.html", context)
