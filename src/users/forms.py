from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, User
from django.contrib.auth.hashers import check_password

from .models import Profile


class UserLoginForm(AuthenticationForm):
    pass


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Username",
            "email": "E-mail",
            "password1": "Password",
            "password2": "Password Confirmation",
        }


# -------------- BAJZEL --------------

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

# -------------- BAJZEL --------------


class UserUsernameUpdateForm(UserChangeForm):
    template_name = "users/forms/generic.html"

    username_confirm = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
        label="Confirm username",
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
            "username": "Username",
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





class UserEmailUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


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
