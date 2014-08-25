from django.conf.urls import patterns, url

from .views import ClipboardFileAPIView, ClipboardImageAPIView
from .forms import ClipboardFileForm, ClipboardImageForm

urlpatterns = patterns(
    '',
    url(r'^images/(?P<pk>\d+)$', ClipboardImageAPIView.as_view(), {'form_class': ClipboardImageForm}, name="clipboard_images"),
    url(r'^images/', ClipboardImageAPIView.as_view(), {'form_class': ClipboardImageForm}, name="clipboard_images"),
    url(r'^(?P<pk>\d+)$', ClipboardFileAPIView.as_view(), {'form_class': ClipboardFileForm}, name="clipboard"),
    url(r'^', ClipboardFileAPIView.as_view(), {'form_class': ClipboardFileForm}, name="clipboard"),
)
