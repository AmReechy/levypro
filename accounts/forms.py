from django import forms
from .models import Payee
from levies.models import LevyType


class PayeeRegistrationForm(forms.ModelForm):

    levy_types = forms.ModelMultipleChoiceField(
        queryset=LevyType.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-checkbox"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input w-full",
                "placeholder": "Create a secure password"
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input w-full",
                "placeholder": "Confirm your password"
            }
        )
    )

    class Meta:
        model = Payee
        fields = [
            "full_name",
            "id_type",
            "id_number",
            "location",
            "phone_number",
            "email",
            #"date_of_birth",
            "address",
            "occupation",
            "passport_photo",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Full Name"
                }
            ),

            "id_type": forms.Select(
                attrs={
                    "class": "form-select w-full"
                }
            ),

            "id_number": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Identification Number"
                }
            ),

            "location": forms.Select(
                attrs={
                    "class": "form-select w-full"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Phone Number"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Email Address"
                }
            ),

            #"date_of_birth": forms.DateInput(
            #   attrs={
            #       "class": "form-input w-full",
            #        "type": "date"
            #    }
            #),

            "address": forms.Textarea(
                attrs={
                    "class": "form-textarea w-full",
                    "rows": 2,
                    "placeholder": "Residential Address"
                }
            ),

            "occupation": forms.TextInput(
                attrs={
                    "class": "form-input w-full",
                    "placeholder": "Occupation"
                }
            ),

            "passport_photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-input w-full"
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password")
        pass2 = cleaned_data.get("confirm_password")
        levy_types = cleaned_data.get("levy_types")
        if pass1 != pass2:
            #raise forms.ValidationError("Passwords do NOT match!")
            self.add_error('confirm_password', "Passwords do NOT match!")
        if not levy_types:
            #raise forms.ValidationError("You MUST choose at least one levy type")
            self.add_error("levy_types", "You MUST choose at least one levy type.")
        return cleaned_data
