from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Category


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': "name@example.com",
                'id': 'floatingInput',
                'type': 'text',
                'class': 'form-control',
                'autocomplete': 'on',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'id': 'floatingPassword',
                'type': 'password',
                'class': 'form-control',
                'autocomplete': 'on',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password',)





class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='first_name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'first_name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='last_name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last_name'})
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        label='username',
        widget=forms.TextInput(
            attrs={
                'placeholder': "name@example.com",
                'type': 'text',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        )
    )


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class PostCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выбрать тему",
        widget=forms.Select(attrs={'class': 'form-select ps-0 py-0 border-0'}),
    )

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control border-0 mb-1', 'placeholder': 'Заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control border-0', 'placeholder': 'Жили были...'}),
            # 'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержимое',
            # 'is_published': 'Опубликовать',
        }
