from django import forms
from .models import Payee
from levies.models import LevyType

class PayeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    levy_types = forms.ModelMultipleChoiceField(
        queryset=LevyType.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Payee
        fields = [
            "full_name", "id_type", "id_number",
            "phone_number", "email", "date_of_birth",
            "address", "occupation", "passport_photo"
        ]
