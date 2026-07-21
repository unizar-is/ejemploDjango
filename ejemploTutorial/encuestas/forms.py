from django import forms
from django.forms import inlineformset_factory

from .models import Pregunta

from .models import Pregunta, Opcion

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["texto_pregunta"]
        widgets = {
            "texto_pregunta": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }


class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ["texto_opcion"]
        widgets = {
            "texto_opcion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Opción"
            }),
        }


OpcionFormSet = inlineformset_factory(
    Pregunta,
    Opcion,
    form=OpcionForm,
    min_num=2,        # Opciones minimas
    extra=0,          # Opciones extra con las que empezar
    can_delete=True,
    #validate_min=True
)