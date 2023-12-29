from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError


def validate_password(password, user_password):
    if not check_password(password, user_password):
        raise ValidationError(
            "Incorrect password. Please try again.", code="invalid", params={"value": password}
        )


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordField, self).__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        validate_password(value, self.user.password)
