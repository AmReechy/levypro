import uuid
from django.db import models
from accounts.models import Payee
from levies.models import LevyType

class Payment(models.Model):
    METHODS = [
        ("CARD", "Card"),
        ("TRANSFER", "Transfer"),
        ("USSD", "USSD"),
    ]

    user = models.ForeignKey(Payee, on_delete=models.CASCADE, related_name="payments")
    levy = models.ForeignKey(LevyType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHODS)
    reference = models.UUIDField(default=uuid.uuid4, unique=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    month = models.DateField()

    verified = models.BooleanField(default=True)
