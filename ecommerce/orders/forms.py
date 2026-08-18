import re

from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "postal_code",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "input", "placeholder": "e.g. Rahul Sharma", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "input", "placeholder": "you@example.com", "autocomplete": "email"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "input", "placeholder": "10-digit mobile number", "autocomplete": "tel"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "input",
                    "rows": 3,
                    "placeholder": "House no., street, area / landmark",
                    "autocomplete": "street-address",
                }
            ),
            "city": forms.TextInput(attrs={"class": "input", "placeholder": "e.g. Meerut"}),
            "state": forms.TextInput(attrs={"class": "input", "placeholder": "e.g. Uttar Pradesh"}),
            "postal_code": forms.TextInput(
                attrs={"class": "input", "placeholder": "6-digit PIN code", "autocomplete": "postal-code"}
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"[0-9+\-\s]{10,15}", phone):
            raise forms.ValidationError("Enter a valid phone number (10–15 digits).")
        return phone

    def clean_postal_code(self):
        pin = self.cleaned_data["postal_code"].strip()
        if not re.fullmatch(r"\d{6}", pin):
            raise forms.ValidationError("Enter a valid 6-digit PIN code.")
        return pin
