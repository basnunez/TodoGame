from django import forms
from django.core import validators
from django.core.validators import RegexValidator

class FormJuego(forms.Form):
    
    enlace = forms.CharField(
        label= "Enlace Zmart",
        min_length=52,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa link de Zmart'
            }
        ),
        validators=[
            validators.MinLengthValidator(limit_value=52, message="En link de Zmart debe tener minimo 52 caracteres"),
        ]
    )

    enlace2 = forms.CharField(
        label = "Enlace Microplay",
        min_length=33,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa link de Microplay'
            }
        )
    ) 

    enlace3 = forms.CharField(
        label = "Enlace Weplay",
        min_length=22,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa link de Weplay'
            }
        )
    )

