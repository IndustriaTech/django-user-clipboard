from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from .utils.ajax import JSONResponse
from .models import Clipboard


def file_as_dict(instance):
        data = {
            'name': instance.filename,
            'id': instance.pk,
            'url': instance.file.url,
        }

        if instance.thumbnail:
            data['thumbnail'] = instance.thumbnail

        return data


class ClipboardFileAPIView(SingleObjectMixin, View):
    model = Clipboard

    def get_queryset(self):
        pk = self.kwargs['pk'] if 'pk' in self.kwargs else None
        if pk:
            return super(ClipboardFileAPIView, self).get_queryset().filter(user=self.request.user, pk=pk)
        else:
            return super(ClipboardFileAPIView, self).get_queryset().filter(user=self.request.user)

    def get(self, request, form_class=None, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        try:
            user_clipboard = self.get_queryset()
        except ObjectDoesNotExist:
            user_clipboard = None

        if user_clipboard:
            data = {
                'data': [file_as_dict(instance) for instance in user_clipboard.iterator()]
            }
            return JSONResponse(request, data)

        return JSONResponse(request, {})

    def post(self, request, form_class=None, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        data = (request.POST, request.FILES)
        instance = Clipboard.objects.get(user=request.user, pk=pk) if pk is not None else None
        form = form_class(*data, instance=instance)

        if form.is_valid():
            form.instance.user = request.user
            instance = form.save()

            try:
                thumb = instance.get_thumbnail_url()
            except:
                thumb = None

            instance.thumbnail = thumb
            instance.save(update_fields=['thumbnail'])

            data = {
                'data': file_as_dict(instance)
            }

            return JSONResponse(request, data)

        return JSONResponse(request, {'errors': form.errors})

    def delete(self, request, form_class=None, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        if pk:
            Clipboard.objects.get(user=request.user, pk=pk).delete()
            return JSONResponse(request, {'success': True})
        else:
            return JSONResponse(request, {'error': "Need a pk for delete"})


class ClipboardImageAPIView(ClipboardFileAPIView):

    def get_queryset(self):
        qs = super(ClipboardImageAPIView, self).get_queryset()
        return qs.filter(user=self.request.user).exclude(thumbnail__isnull=True)
