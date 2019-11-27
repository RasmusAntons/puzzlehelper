from django import forms


class UrlfinderForm(forms.Form):
    query = forms.CharField(label='Query', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Query'}))
