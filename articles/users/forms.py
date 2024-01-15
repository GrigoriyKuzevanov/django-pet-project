import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)

from users.tasks import send_mail_to_user_task


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(
        label="Повторить пароль", widget=forms.PasswordInput()
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "email": "E-mail",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    # def clean_password_repeat(self):
    #     cd = self.cleaned_data
    #     if cd["password"] != cd["password_repeat"]:
    #         raise forms.ValidationError("Пароли не совпадают!")
    #     return cd["password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if (
            get_user_model().objects.filter(email=email).exists()
        ):  # проверка на существование в базе данных пользователя с введенным почтовым адресом
            raise forms.ValidationError("Указанный e-mail уже существует")
        return email
    
    def send_email(self):
        user = self.cleaned_data["username"]
        subject = "DJ-Blog registration"
        message = f"""
        Congratulations! You've successfully registered on the DJ-Blog website!
        Your login for enter the site is <{user}>
        """
        email = self.cleaned_data["email"]
        send_mail_to_user_task.delay(email, message, subject)


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин", widget=forms.TextInput())
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput())
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))

    class Meta:
        model = get_user_model()
        fields = [
            "photo",
            "username",
            'email',
            "first_name",
            "last_name",
            "date_birth",
        ]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }


class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput())
