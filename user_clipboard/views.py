from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from .utils.ajax import JSONResponse
from .models import Clipboard
from .forms import ClipboardFileForm, ClipboardImageForm


def file_as_dict(instance):
        data = {
            'id': instance.pk,
            'name': instance.filename,
            'url': instance.file.url,
        }

        if instance.is_image:
            data['thumbnail'] = instance.get_thumbnail_url()

        return data


class ClipboardFileAPIView(SingleObjectMixin, View):
    model = Clipboard
    form_class = ClipboardFileForm

    def get_queryset(self):
        return super(ClipboardFileAPIView, self).get_queryset().filter(user=self.request.user)

    def get(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        if pk is None:
            user_clipboard = self.get_queryset()
            data = {
                'data': [file_as_dict(instance) for instance in user_clipboard.iterator()]
            }

        else:
            user_clipboard = self.get_object()
            data = {
                'data': [file_as_dict(user_clipboard)]
            }

        return JSONResponse(request, data)

    def post(self, request, form_class=None, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        data = (request.POST, request.FILES)

        instance = self.get_object() if pk is not None else None

        form = self.form_class(*data, instance=instance)

        if form.is_valid():
            form.instance.user = request.user
            instance = form.save()

            data = {
                'data': file_as_dict(instance)
            }

            return JSONResponse(request, data)

        return JSONResponse(request, {'errors': form.errors})

    def delete(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        try:
            self.get_object().delete()
            return JSONResponse(request, {'success': True})
        except Exception as e:
            return JSONResponse(request, {'error': str(e)})


class ClipboardImageAPIView(ClipboardFileAPIView):
    form_class = ClipboardImageForm

    def get_queryset(self):
        qs = super(ClipboardImageAPIView, self).get_queryset()
        return qs.filter(is_image=True)
