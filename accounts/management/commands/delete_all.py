

from django.core.management.base import BaseCommand
from accounts.models import Payee
class Command(BaseCommand):
    help = "Delete ALL MAJOR tables in the database:Payees, Payments and Receipts."
    
    def handle(self, *args, **options):
        from accounts.models import Payee
        from payments.models import Payment
        from payments.receipt import Receipt

        try:
            rs = Receipt.objects.all()
            print(rs.delete())
            ps = Payment.objects.all()
            print(ps.delete())
            payees = Payee.objects.all()
            print(payees.delete())

            self.stdout.write(
                self.style.SUCCESS(f"Successfully deleted payee with ID number '{id_number}' along with their associated Payments and corresponding receipts")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"ERROR: {e} !"
                ))
            
