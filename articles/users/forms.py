from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password_repeat = forms.CharField(
        label="Повторить пароль", widget=forms.PasswordInput()
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_repeat",
        ]
        labels = {
            "email": "E-mail",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password_repeat"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd["password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if (
            get_user_model().objects.filter(email=email).exists()
        ):  # проверка на существование в базе данных пользователя с введенным почтовым адресом
            raise forms.ValidationError("Указанный e-mail уже существует")
        return email
