from django import forms
from codes.models import Tag
from multiupload.fields import MultiImageField


class BarcodeEditForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Description'}), help_text='Markdown enabled.')
    resources = forms.CharField(label='Resources', widget=forms.Textarea(attrs={'placeholder': 'Resources'}), help_text='Markdown enabled.')
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, help_text='Multiple files allowed.')
