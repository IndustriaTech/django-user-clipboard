from django import forms

from .models import Clipboard


class BaseClipboardForm(object):
    def save(self, commit=True):
        # Delete old file before saving the new one
        if self.instance.pk:
            old_instance = self._meta.model.objects.get(pk=self.instance.pk)
            old_instance.file.delete(save=False)
        return super(BaseClipboardForm, self).save(commit=commit)


class ClipboardFileForm(BaseClipboardForm, forms.ModelForm):
    class Meta:
        model = Clipboard
        fields = ('file',)


class ClipboardImageForm(ClipboardFileForm):
    file = forms.ImageField()
