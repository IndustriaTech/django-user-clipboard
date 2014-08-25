import uuid

from django.db import models
from django.contrib.auth.models import User

from easy_thumbnails.files import get_thumbnailer


def new_file_upload_to(instance, filename):
    """Generate file path for newly uploaded files"""
    instance.filename = filename
    ext = filename.split('.')[-1]
    uid = instance.user_id
    return "clipboard/%(uid)s/%(name)s.%(ext)s" % {
        'uid': uid,
        'name': uuid.uuid4(),
        'ext': ext,
    }


class Clipboard(models.Model):
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=new_file_upload_to, max_length=255)
    filename = models.CharField(max_length=128, null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.file.name

    def get_thumbnail_url(self):
        if self.file:
            thumbnailer = get_thumbnailer(self.file)
            thumbnail_options = {'size': (100, 100), 'crop': True}
            img_thumb = thumbnailer.get_thumbnail(thumbnail_options)
            return img_thumb.url
