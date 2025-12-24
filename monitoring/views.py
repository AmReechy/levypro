from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.utils.timezone import now
from django.shortcuts import render

from accounts.models import Payee
from payments.models import Payment

@staff_member_required
def admin_dashboard(request):
    current_month = now().month
    current_year = now().year

    total_payees = Payee.objects.count()
    total_revenue = Payment.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    monthly_payments = Payment.objects.filter(
        paid_at__month=current_month,
        paid_at__year=current_year
    ).count()

    compliant_users = Payment.objects.filter(
        paid_at__month=current_month,
        paid_at__year=current_year
    ).values("user").distinct().count()

    compliance_rate = (
        (compliant_users / total_payees) * 100
        if total_payees > 0 else 0
    )

    levy_breakdown = (
        Payment.objects
        .values("levy__name")
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
        )
        .order_by("month")
    )

    context = {
        "total_payees": total_payees,
        "total_revenue": total_revenue,
        "monthly_payments": monthly_payments,
        "compliance_rate": round(compliance_rate, 2),
        "levy_breakdown": levy_breakdown,
        "monthly_trend": monthly_trend,
    }

    return render(request, "monitoring/admin_dashboard.html", context)
