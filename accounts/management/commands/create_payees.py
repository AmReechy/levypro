import random
from datetime import date

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker

from accounts.models import Payee
from levies.models import LevyType  # adjust import if needed

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with fake Payee users: total  start_num"

    def add_arguments(self, parser):
        # Positional arguments (required)
        parser.add_argument('total', type=int, help='Indicates the number of users to be created') #

        # Optional arguments (named)
        parser.add_argument(
            'start_num',
            type=int,
            default=1,
            help='Define the number to start the payee id from'
        )

    def handle(self, *args, **options):
        PASSWORD = "@password"
        TOTAL_PAYEES = options['total']
        START_NUM = options['start_num']

        levy_types = list(LevyType.objects.all())
        if not levy_types:
            self.stdout.write(self.style.ERROR(
                "No LevyType found. Please create levy types first."
            ))
            return

        created_count = 0

        for i in range(START_NUM, START_NUM +  TOTAL_PAYEES):
            id_number = str(i).zfill(5)   # 00001 → 00100
            phone_number = id_number
            email = f"payee{id_number}@example.com"

            if Payee.objects.filter(id_number=id_number).exists():
                continue

            payee = Payee.objects.create_user(
                id_number=id_number,
                phone_number=phone_number,
                email=email,
                password=PASSWORD,
                id_type=random.choice(["NIN", "TIN", "BVN", "PHONE"]),
                full_name=fake.name(),
                #date_of_birth=fake.date_of_birth(
                #minimum_age=18, maximum_age=70
                #),
                location=random.choices(
                    population=["Wuse", "Garki", "Maitama", "Gwarinpa", "Nyanya", "Asokoro", "Utako", "Karu"],
                    weights=[0.25,0.15,0.35,0.05,0.05,0.05,0.5,0.5])[0],
                address=fake.address(),
                occupation=fake.job(),
                is_active=True,
            )

            # Assign 1–3 levy types (mostly 1 or 2)
            num_levies = random.choices(
                population=[1, 2, 3],
                weights=[0.6, 0.3, 0.1],
                k=1
            )[0]

            payee.levy_types.set(random.sample(levy_types, num_levies))

            # Fake passport photo
            fake_image = ContentFile(b"", name=f"passport_{id_number}.jpg")
            payee.passport_photo.save(
                f"passport_{id_number}.jpg",
                fake_image,
                save=True
            )

            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f"Created payee {id_number}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\n✔ Successfully created {created_count} payees")
        )

