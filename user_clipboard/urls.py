from django.conf.urls import url

from .views import ClipboardFileAPIView, ClipboardImageAPIView

urlpatterns = [
    url(r'^images/(?P<pk>\d+)/$', ClipboardImageAPIView.as_view(), name="clipboard_images"),
    url(r'^images/$', ClipboardImageAPIView.as_view(), name="clipboard_images"),
    url(r'^(?P<pk>\d+)$', ClipboardFileAPIView.as_view(), name="clipboard"),
    url(r'^', ClipboardFileAPIView.as_view(), name="clipboard"),
]
