from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    User,
)


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



