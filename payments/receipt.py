import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models

class Receipt(models.Model):
    payment = models.OneToOneField("Payment", on_delete=models.CASCADE, related_name="receipt")
    qr_code = models.ImageField(upload_to="qr_receipts/")
    created = models.DateTimeField(auto_now_add=True)

    def generate(self):
        data = f"""
        PAYEE: {self.payment.user.full_name}
        LEVY: {self.payment.levy.name}
        AMOUNT: {self.payment.amount}
        REF: {self.payment.reference}
        """

        img = qrcode.make(data)
        buffer = BytesIO()
        img.save(buffer)
        self.qr_code.save(
            f"{self.payment.reference}.png",
            File(buffer),
            save=False
        )
