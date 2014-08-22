from django import forms

from .models import Clipboard


class ClipboardFileForm(forms.ModelForm):
    class Meta:
        model = Clipboard
        fields = ('file',)


class ClipboardImageForm(forms.ModelForm):

    file = forms.ImageField()

    class Meta:
        model = Clipboard
        fields = ('file',)
