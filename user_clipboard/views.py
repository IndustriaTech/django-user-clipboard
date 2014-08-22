from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.generic import View

from .utils.ajax import JSONResponse
from .models import Clipboard
from .forms import ClipboardFileForm, ClipboardImageForm


def file_as_dict(instance):
        data = {
            'name': instance.filename,
            'id': instance.pk,
            'url': instance.file.url,
        }

        if instance.thumbnail:
            data['thumbnail'] = instance.thumbnail

        return data


class ClipboardFileAPIView(View):

    def get(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        if pk:
            try:
                user_clipboard = Clipboard.objects.filter(user=request.user, pk=pk)
            except ObjectDoesNotExist:
                user_clipboard = None

        else:
            try:
                user_clipboard = Clipboard.objects.filter(user=request.user)
            except ObjectDoesNotExist:
                user_clipboard = None

        if user_clipboard:
            data = {
                'data': [file_as_dict(instance) for instance in user_clipboard.iterator()]
            }

            return JSONResponse(request, data)

        return JSONResponse(request, {})

    def post(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        data = (request.POST, request.FILES)
        form = ClipboardFileForm(*data)

        if form.is_valid():
            try:
                instance = Clipboard.objects.get(user=request.user, pk=pk)
            except ObjectDoesNotExist:
                instance = None

            if instance:
                instance.file = request.FILES['file']
                instance.save()

            else:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()

            data = {
                'data': {
                    'name': instance.filename,
                    'url': instance.file.url,
                }
            }

            try:
                thumb = instance.get_thumbnail_url()
            except:
                thumb = None

            instance.thumbnail = thumb
            instance.save(update_fields=['thumbnail'])

            if instance.thumbnail:
                data['data']['thumbnail'] = instance.thumbnail

            return JSONResponse(request, data)

        return JSONResponse(request, {'errors': form.errors})

    def delete(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        if pk:
            Clipboard.objects.get(user=request.user, pk=pk).delete()
            return JSONResponse(request, {'success': True})
        else:
            return JSONResponse(request, {'error': "Need a pk for delete"})


class ClipboardImageAPIView(View):

    def get(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        if pk:
            try:
                user_clipboard = Clipboard.objects.filter(user=request.user, pk=pk)
            except ObjectDoesNotExist:
                user_clipboard = None

        else:
            try:
                user_clipboard = Clipboard.objects.filter(user=request.user).exclude(thumbnail__isnull=True)
            except ObjectDoesNotExist:
                user_clipboard = None

        if user_clipboard:
            data = {
                'data': [file_as_dict(instance) for instance in user_clipboard.iterator()]
            }

            return JSONResponse(request, data)

        return JSONResponse(request, {})

    def post(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied

        data = (request.POST, request.FILES)
        form = ClipboardImageForm(*data)

        if form.is_valid():
            try:
                instance = Clipboard.objects.get(user=request.user, pk=pk)
            except ObjectDoesNotExist:
                instance = None

            if instance:
                instance.file = request.FILES['file']
                instance.save()

            else:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()

            instance.thumbnail = instance.get_thumbnail_url()
            instance.save(update_fields=['thumbnail'])

            data = {
                'data': {
                    'name': instance.filename,
                    'id': instance.pk,
                    'thumbnail': instance.thumbnail,
                    'url': instance.file.url,
                }
            }

            return JSONResponse(request, data)

        return JSONResponse(request, {'errors': form.errors})

    def delete(self, request, pk=None):
            if not request.user.is_authenticated():
                raise PermissionDenied
            if pk:
                Clipboard.objects.get(user=request.user, pk=pk).delete()
                return JSONResponse(request, {'success': True})
            else:
                return JSONResponse(request, {'error': "Need a pk for delete"})
