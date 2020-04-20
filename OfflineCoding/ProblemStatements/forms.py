from django import forms

class InputForm(forms.Form):

        DIFFICULTY = (
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        )

        start = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'Starting index'
        }), label='')
        end = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ending index'
        }), label='')

        difficulty = forms.ChoiceField(choices=DIFFICULTY, widget=forms.Select(attrs={
            'class': 'form-control'
        }), required=False, label="Difficulty")

        field_order = ['start','end','difficulty']
