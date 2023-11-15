from django import forms
from django.contrib.auth.forms import UserChangeForm
from startpage.models import Order, DeliveryOption, Address


class AdressForms(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'hause', 'apartment']

