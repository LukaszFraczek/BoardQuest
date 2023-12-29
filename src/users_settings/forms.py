from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    UserChangeForm,
    PasswordChangeForm,
    User,
)

from .form_validation import PasswordField
from users.models import Profile


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'about_me']
        widgets = {
            'image': forms.FileInput,
            'about_me': forms.Textarea(attrs={
                "class": "form-control",
                'placeholder': 'Say something about yourself! :)'}),
        }


class UserUsernameUpdateForm(UserChangeForm):
    template_name = "users/forms/generic.html"

    username_confirm = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
        label="New username confirmation",
        required=True,
    )
    password_confirm = PasswordField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label="Password",
        required=True,
    )
    password = None

    field_order = ['username', 'username_confirm', 'password_confirm']

    class Meta:
        model = User
        fields = ['username']
        labels = {
            "username": "New username",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserUsernameUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password_confirm'].user = self.user  # MAKE BETTER

    def clean_username(self):
        new_username = self.cleaned_data.get('username')

        # Check if entered username is unique
        if User.objects.filter(username=new_username).exclude(pk=self.user.pk).exists():
            raise ValidationError("Username taken. Please choose a different one.")

        # Check if entered username is users' current username
        if new_username == self.user.username:
            raise ValidationError("You already have this username!")

        return new_username

    def clean(self):
        cleaned_data = super().clean()
        new_username = cleaned_data.get('username')
        new_username_conf = cleaned_data.get('username_confirm')

        # Check if entered usernames are the same
        if new_username != new_username_conf:
            raise ValidationError("Usernames do not match each other.")

        return cleaned_data


class UserEmailUpdateForm(UserChangeForm):
    template_name = "users/forms/generic.html"

    email_confirm = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "type": "email"}),
        label="New email confirmation",
        required=True,
    )
    password_confirm = PasswordField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label="Password",
        required=True,
    )
    password = None

    field_order = ['email', 'email_confirm', 'password_confirm']

    class Meta:
        model = User
        fields = ['email']
        labels = {
            "email": "New email",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "type": "email"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserEmailUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password_confirm'].user = self.user  # MAKE BETTER

    def clean_email(self):
        new_email = self.cleaned_data.get('email')

        # Check if entered email is unique (case INSENSITIVE!)
        if User.objects.filter(email__iexact=new_email).exclude(pk=self.user.pk).exists():
            raise ValidationError("Provided email already in use!")

        # Check if entered username is users' current username (case INSENSITIVE!)
        if new_email.upper() == self.user.email.upper():
            raise ValidationError("You already have this email!")

        return new_email

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get('email')
        new_email_conf = cleaned_data.get('email_confirm')

        # Check if entered usernames are the same
        if new_email != new_email_conf:
            raise ValidationError("Provided emails do not match each other.")

        return cleaned_data


class UserPasswordUpdateForm(PasswordChangeForm):
    template_name = "users/forms/generic.html"

    field_order = ["new_password1", "new_password2", "old_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        new_password_widget = forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "type": "password",
            }
        )
        old_password_widget = forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
                "type": "password",
            }
        )
        self.fields['new_password1'].widget = new_password_widget
        self.fields['new_password2'].widget = new_password_widget
        self.fields['old_password'].widget = old_password_widget
