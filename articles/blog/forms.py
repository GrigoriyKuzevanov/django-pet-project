from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from .models import Category, Author, Post
from string import printable, ascii_letters


@deconstructible
class AsciiValidator:
    """
    Валидатор для текстовых полей: 
    разрешены только символы из коллекции ascii.printable
    """
    ALLOWED = ascii_letters
    code = 'ascii.printable'

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Ошибка ввода: '

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED)):
            NOT_ALLOWED = set(value).difference(set(self.ALLOWED))
            message = f"cимволы ({' '.join(NOT_ALLOWED)}) не допускаются!"
            raise ValidationError(message=self.message + message, code=self.code)


class AddPostForm(forms.ModelForm):
    """
    Класс для формы добавления нового поста
    """
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label='Автор', empty_label='Автор не выбран')    # required=False делает поле необязательным


    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'is_published', 'category', 'author']  # поля модели, отображаемые в форме ('__all__' - все)
        widgets = {
            'title': forms.TextInput(),
            'content': forms.Textarea()
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        validator = AsciiValidator()
        title = self.cleaned_data['title']
        validator(title)
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")
