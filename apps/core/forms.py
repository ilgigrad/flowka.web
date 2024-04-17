from django import forms

class MultipleForm(forms.ModelForm):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())
