from typing import Any, Dict
from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        widget=forms.EmailInput({"class": "form-control"}), required=True)
    password = forms.CharField(
        widget=forms.PasswordInput({"class": "form-control"}), required=True)

    def clean(self) -> Dict[str, Any]:
        clean_data = super().clean()
        user = authenticate(
            self.request,
            username=clean_data["email"],
            password=clean_data['password'])

        if user is not None:
            clean_data['user'] = user
            return clean_data
        else:
            raise forms.ValidationError('credential is invalid')
