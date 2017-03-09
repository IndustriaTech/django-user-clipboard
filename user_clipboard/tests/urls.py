from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from user_clipboard.forms import ClipboardFileForm, ClipboardImageForm

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('user_clipboard.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), {'file_form': ClipboardFileForm(),
                                                                  'image_form': ClipboardImageForm()}),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ]
