from django import forms
from .models import Signoff


class SignoffForm(forms.ModelForm):
    class Meta:
        model = Signoff
        fields = ['name', 'qnt', 'unit']