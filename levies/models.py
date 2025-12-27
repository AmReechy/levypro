from django.db import models

# Create your models here.


class LevyType(models.Model):
    name = models.CharField(max_length=50)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

create_levy_types = '''
lts = [("Property Levy", 10000), ("Restaurant Levy", 15000), ("Shop Levy", 5000), ("Commercial Car Levy", 3000)]
for l in lts:
    name = l[0]
    amount= l[1]
    LevyType.objects.create(name=name, monthly_amount=amount)
'''
