
from django.core.management.base import BaseCommand
from accounts.models import Payee
class Command(BaseCommand):
    help = "Seed database with fake Payee users: total  start_num"

    def add_arguments(self, parser):
        # Positional arguments (required)
        parser.add_argument('total', type=int, help='Indicates the number of payees to be deleted') #

        # Optional arguments (named)
        parser.add_argument(
            'id_or_start_num',
            #type=int,
            #default=1,
            help='Define the payee ID to start deleting from'
        )

    def handle(self, *args, **options):
        total_to_del = options.get("total")
        id_or_start_num = options.get("id_or_start_num")
        if total_to_del < 1:
            self.stdout.write(self.style.ERROR(
                f"Number of payees to delete must be at least one, you specified '{total_to_del}'"
            ))
            return
        if total_to_del == 1:
            try:
                payee = Payee.objects.get(id_number=id_or_start_num)
                payee.delete()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully deleted payee with ID number '{id_number}' along with their associated Payments and corresponding receipts")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Either \nThere is no payee with the specified ID number '{id_or_start_num}'\nOr\n{e}"
                    ))
            return
        else:
            try:
                start_ind = int(id_or_start_num)
                for i in range(start_ind, start_ind + total_to_del):
                    try:
                        id_num = str(i).zfill(5)
                        payee = Payee.objects.get(id_number=id_num)
                        payee.delete()
                        self.stdout.write(
                            self.style.SUCCESS(f"Successfully deleted payee with ID number '{id_num}' along with their associated Payments and corresponding receipts")
                        )
                    except Payee.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f"There is no payee with the specified ID number '{id_num}'"
                            ))
                        continue
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f"Error: {e} !"
                            ))
                        return
            except ValueError as e:
                self.stdout.write(self.style.ERROR(
                    f"Error: {e} !"
                    ))
                return


    
