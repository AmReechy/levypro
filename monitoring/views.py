from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, F
from django.utils.timezone import now
from django.shortcuts import render

from accounts.models import Payee
from payments.models import Payment
from levies.models import LevyType
from django.contrib import messages

@staff_member_required
def admin_dashboard(request):
    current_month = now().month
    current_year = 2025 #now().year

    total_payees = Payee.objects.count()
    total_revenue = Payment.objects.filter(month__year= current_year).aggregate(
        total=Sum("amount")
    )["total"] or 0

    monthly_payments = Payment.objects.filter(
        #paid_at__month=current_month,
        paid_at__year=current_year,
        month__month=current_month
    ).count()

    monthly_expected_payments = 0
    monthly_expected_revenue = 0
    payees = Payee.objects.all()
    for p in payees:
        monthly_expected_payments += p.levy_types.count()
    levy_types = LevyType.objects.all()
    for lt in levy_types:
        tot_payees = Payee.objects.filter(levy_types=lt).count()
        tot_payments = tot_payees * lt.monthly_amount
        monthly_expected_revenue += tot_payments

    #print(monthly_expected_payments)

    total_payments_year = Payment.objects.filter(month__year= current_year).count()
    total_months_considered = Payment.objects.filter(month__year= current_year).values("month").distinct().count()
    expected_payments_year = total_months_considered * monthly_expected_payments
    """compliant_users = Payment.objects.filter(
        paid_at__month=current_month,
        paid_at__year=current_year
    ).values("user").distinct().count()

    compliance_rate = (
        (compliant_users / total_payees) * 100
        if total_payees > 0 else 0
    )
    """

    avg_compliance_rate = round(total_payments_year/expected_payments_year * 100, 2)

    levy_breakdown = (
        Payment.objects
        .values("levy__name")
        .annotate(
            count=Count("id"),
            amount=Sum("amount")
        )
    )

    levy_breakdown_location = (
        Payment.objects
        .values("user__location")
        .annotate(
            count=Count("id"),
            amount=Sum("amount")
        )
    )

    monthly_trend = (
        Payment.objects
        .values("month")
        .annotate(
            count=Count("id"),
            amount=Sum("amount")
        ).annotate(
            compliance=F("count") * 100.0 /monthly_expected_payments
            )
        .order_by("month")
    )

    #print(monthly_trend)

    context = {
        "total_payees": total_payees,
        "total_revenue": total_revenue,
        "monthly_payments": monthly_payments,
        "avg_compliance_rate": avg_compliance_rate,
        "levy_breakdown": levy_breakdown,
        "location_breakdown": levy_breakdown_location,
        "monthly_trend": monthly_trend,
        "monthly_expected_payments": monthly_expected_payments,
        "monthly_expected_revenue": monthly_expected_revenue,
        "tot_months_considered": total_months_considered 
    }

    return render(request, "admin_dashboard.html", context)
