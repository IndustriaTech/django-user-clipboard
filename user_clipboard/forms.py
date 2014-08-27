from django import forms

from .models import Clipboard


class ClipboardFileForm(forms.ModelForm):
    class Meta:
        model = Clipboard
        fields = ('file',)

    def save(self, commit=True):
        # Delete old file before saving the new one
        if self.instance.pk:
            old_instance = self._meta.model.objects.get(pk=self.instance.pk)
            old_instance.file.delete(save=False)
        return super(ClipboardFileForm, self).save(commit=commit)


class ClipboardImageForm(ClipboardFileForm):
    file = forms.ImageField()
