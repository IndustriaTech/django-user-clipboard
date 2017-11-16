import django
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from .utils.ajax import JSONResponse
from .models import Clipboard
from .forms import ClipboardFileForm, ClipboardImageForm


if django.VERSION < (1, 11):
    def is_authenticated(user):
        return user.is_authenticated()
else:
    def is_authenticated(user):
        return user.is_authenticated


class ClipboardFileAPIView(SingleObjectMixin, View):
    model = Clipboard
    form_class = ClipboardFileForm

    def get_queryset(self):
        return super(ClipboardFileAPIView, self).get_queryset().filter(user=self.request.user)

    def get(self, request, pk=None):
        if not is_authenticated(request.user):
            raise PermissionDenied

        if pk is None:
            return JSONResponse(request, {
                'data': [
                    self.file_as_dict(instance)
                    for instance in self.get_queryset().iterator()
                ]
            })

        return JSONResponse(request, {
            'data': self.file_as_dict(self.get_object())
        })

    def post(self, request, pk=None):
        if not is_authenticated(request.user):
            raise PermissionDenied

        instance = self.get_object() if pk is not None else None
        form = self.form_class(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.instance.user = request.user
            instance = form.save()
            return JSONResponse(request, {
                'data': self.file_as_dict(instance)
            })

        return JSONResponse(request, {'errors': form.errors}, status=400)

    def delete(self, request, pk=None):
        if not is_authenticated(request.user):
            raise PermissionDenied
        if pk is None:
            # Clear the clipboard
            self.get_queryset().delete()
        else:
            self.get_object().delete()
        return JSONResponse(request, {'success': True})

    def file_as_dict(self, instance):
        data = {
            'id': instance.pk,
            'name': instance.filename,
            'url': instance.file.url,
        }

        if instance.is_image:
            data['thumbnail'] = instance.get_thumbnail_url()

        return data


class ClipboardImageAPIView(ClipboardFileAPIView):
    form_class = ClipboardImageForm

    def get_queryset(self):
        qs = super(ClipboardImageAPIView, self).get_queryset()
        return qs.filter(is_image=True)
