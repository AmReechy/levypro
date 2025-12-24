from django.db import models

# Create your models here.


class LevyType(models.Model):
    name = models.CharField(max_length=50)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

levy_types = '''
LevyType.objects.bulk_create([
    LevyType(name="Property Levy", monthly_amount=10000),
    LevyType(name="Restaurant Levy", monthly_amount=15000),
    LevyType(name="Shop Levy", monthly_amount=5000),
    LevyType(name="Commercial Car Levy", monthly_amount=3000),
])
'''
