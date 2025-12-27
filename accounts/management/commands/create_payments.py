import random
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from accounts.models import Payee
from payments.models import Payment
from payments.receipt import Receipt
from levies.models import LevyType


class Command(BaseCommand):
    help = "Seed fake monthly payments for payees"

    def handle(self, *args, **options):
        MONTHS_BACK = 12
        COMPLIANCE_RATE = 0.8  # 80% chance a payee pays in a given month

        payment_methods = ["CARD", "TRANSFER", "USSD"]

        payees = Payee.objects.prefetch_related("levy_types")

        if not payees.exists():
            self.stdout.write(self.style.ERROR("No payees found"))
            return

        today = date.today().replace(day=1)
        created = 0

        for payee in payees:
            levies = list(payee.levy_types.all())
            if not levies:
                continue

            for i in range(MONTHS_BACK):
                month = today - relativedelta(months=i)

                # Simulate non-compliance
                if random.random() > COMPLIANCE_RATE:
                    continue

                for levy in levies:
                    # Prevent duplicates
                    if Payment.objects.filter(
                        user=payee,
                        levy=levy,
                        month=month
                    ).exists():
                        continue

                    payment = Payment.objects.create(
                        user=payee,
                        levy=levy,
                        amount=Decimal(levy.monthly_amount),
                        method=random.choice(payment_methods),
                        month=month,
                        verified=random.choices(
                            [True, False],
                            weights=[0.90, 0.10],
                            k=1
                        )[0]
                    )

                    receipt = Receipt.objects.create(payment=payment)
                    receipt.generate()
                    receipt.save()

                    created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✔ Successfully created payment for {payee.id_number} ({payee.full_name})"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ Successfully created {created} fake payments"
            )
        )

