from django import forms
from . import models


class ShopForm(forms.ModelForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=True,
        required=False,
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'type': 'text',
                'placeholder': 'Название'
            }
        ),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                'type': 'textarea',
                'style': 'height: 100px',
                'placeholder': 'Описание'
            }
        ),
        required=False,
    )

    logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'type': 'file',
            }
        )
    )

    source = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'value': "shop_form"}
        )
    )

    class Meta:
        model = models.Shop
        fields = ('title', 'is_active')




class WarehouseForm(forms.ModelForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=True,
        required=False,
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'type': 'text',
            },
        ),
        required=True,
    )

    shop = forms.ModelChoiceField(
        queryset=models.Shop.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        required=True,
    )

    source = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'value': "warehouse_form"}
        )
    )
    class Meta:
        model = models.Warehouse
        fields = ('title', 'source', 'shop')


class ItemForm(forms.ModelForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=True,
        required=False,
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'type': 'text',
            },
        ),
        required=True,
    )

    shop = forms.ModelChoiceField(
        queryset=models.Shop.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        required=True,
    )

    category = forms.ModelChoiceField(
        queryset=models.ItemCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        required=True,
    )

    sku = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'type': 'text',
            }
        )
    )

    source = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'value': "item_form"}
        )
    )
    class Meta:
        model = models.Item
        fields = ('title', 'source', 'shop', 'category', 'sku')


class CategoryForm(forms.ModelForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=True,
        required=False,
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'type': 'text',
            },
        ),
        required=True,
    )

    parent = forms.ModelChoiceField(
        queryset=models.ItemCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',

            }
        )
    )

    properties = forms.ModelMultipleChoiceField(
        queryset=models.ItemProperty.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
            }
        )
    )

    shop = forms.ModelChoiceField(
        queryset=models.Shop.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        required=True,
    )

    class Meta:
        model = models.ItemCategory
        fields = ['is_active', 'title', 'parent', 'properties', 'shop']



class ItemPropertyForm(forms.ModelForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=True,
        required=False,
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'type': 'text',
                'placeholder': '',
            },
        ),
        required=True,
    )

    is_aspect = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=False,
        required=False,
    )

    is_required = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=False,
        required=False,
    )
    is_multiply = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=False,
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                'placeholder': '',
            }
        ),
        required=False,
    )

    # shop = forms.ModelChoiceField(
    #     queryset=models.Shop.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-select',
    #             'placeholder': '',
    #         }
    #     )
    # )

    # category = forms.ModelChoiceField(
    #     queryset=models.ItemCategory.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-select',
    #         }
    #     )
    # )


    type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'type': 'text',
            }
        ),
        choices=models.PropertyType,
        required=True,
    )

    class Meta:
        model = models.ItemProperty
        fields = ('is_active', 'title', 'is_aspect', 'is_required', 'description', 'is_multiply', 'type')


class ItemPropertyValueForm(forms.ModelForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                'type': 'checkbox',
            }
        ),
        initial=True,
        required=False,
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'type': 'text',
            },
        ),
        required=False,
    )

    property = forms.ModelChoiceField(
        queryset=models.ItemProperty.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        required=False,
    )

    class Meta:
        model = models.ItemPropertyValue
        fields = ('is_active', 'title', 'property')

