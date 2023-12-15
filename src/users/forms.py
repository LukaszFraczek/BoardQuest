from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User


class UserLoginForm(AuthenticationForm):
    pass


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Custom field labels
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'E-mail'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password Confirmation'

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
