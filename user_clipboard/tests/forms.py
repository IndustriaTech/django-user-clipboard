from django import forms
from user_clipboard.models import Clipboard
from .models import ModelWithFile, ModelWithImage


class ModelWithFileForm(forms.ModelForm):

    document = forms.IntegerField()

    class Meta:
        model = ModelWithFile
        fields = 'document',

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ModelWithFileForm, self).__init__(*args, **kwargs)

    def clean_document(self):
        clipboard_pk = self.cleaned_data['document']
        if clipboard_pk:
            try:
                item = Clipboard.objects.get(pk=clipboard_pk, user=self.user)
                return item.get_file()
            except Clipboard.DoesNotExist:
                raise forms.ValidationError('Error processing document. Please upload it again.')
        return None


class ModelWithImageForm(forms.ModelForm):

    image = forms.IntegerField()

    class Meta:
        model = ModelWithImage
        fields = 'image',

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ModelWithImageForm, self).__init__(*args, **kwargs)

    def clean_image(self):
        clipboard_pk = self.cleaned_data['image']
        if clipboard_pk:
            try:
                item = Clipboard.objects.get(pk=clipboard_pk, user=self.user)
                return item.get_image()
            except Clipboard.DoesNotExist:
                raise forms.ValidationError('Error processing image. Please upload it again.')
        return None
