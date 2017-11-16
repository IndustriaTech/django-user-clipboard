from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from user_clipboard.forms import ClipboardFileForm, ClipboardImageForm
from .views import upload_document, upload_image

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('user_clipboard.urls')),
    url(r'^documents/', upload_document, name='test_user_clipboard_upload_document'),
    url(r'^images/', upload_image, name='test_user_clipboard_upload_image'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), {'file_form': ClipboardFileForm(),
                                                                  'image_form': ClipboardImageForm()}),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ]
