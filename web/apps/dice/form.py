from django import forms
from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse


class DiceForm(forms.Form):
    template_name = "dice/form/field.html"

    DEFAULT_DIES, DEFAULT_SIDES = 7, 50

    dies = forms.IntegerField(
        min_value=0,
        max_value=99,
        label="Dies",
        required=True,
        initial=DEFAULT_DIES,
    )

    sides = forms.IntegerField(
        min_value=2,
        max_value=99,
        label="Sides",
        required=True,
        initial=DEFAULT_SIDES,
    )
