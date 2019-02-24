from django import forms
from .validators import CustomURLValidator


class ShortenerForm(forms.Form):
    """ Form that allows passing URLs with schemes: 'http', 'https', ''."""

    # Custom validator to allow only urls with following schemes.
    validator = CustomURLValidator(schemes=['http', 'https', ''])

    # CharField for URL.
    url = forms.CharField(max_length=255,
                          label="",
                          validators=[validator],
                          widget=forms.TextInput(attrs={'placeholder': 'URL'}))
