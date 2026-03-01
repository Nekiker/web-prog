from django import forms
from .models import Category, ShipPassport
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from .validators import forbidden_words
from .models import Starship, Category, ShipPassport
from django.core.exceptions import ValidationError

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Категория не выбрана",
        label="Категории"
    )

    passport = forms.ModelChoiceField(
        queryset=ShipPassport.objects.all(),
        required=False,
        empty_label="Техпаспорт не выбран",
        label="Техпаспорт"
    )

    class Meta:
        model = Starship
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'passport', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title