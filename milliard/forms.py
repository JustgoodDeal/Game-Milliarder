from django import forms
from .models import Player
from django.core.exceptions import ValidationError
import re

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name','count_correct_answers', 'money_won']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }

    def clean_name(self):
        new_name = self.cleaned_data['name']
        if not re.match (r'^[а-яА-ЯёЁa-zA-Z\s]+$', new_name):
            raise ValidationError('В имени могут содержаться только буквы')
        return new_name  