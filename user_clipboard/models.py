import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


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
    image_thumbnail = ImageSpecField(source='file',
                                     processors=[ResizeToFill(settings.CLIPBOARD_IMAGE_WIDTH, settings.CLIPBOARD_IMAGE_HEIGHT)],
                                     format='JPEG',
                                     options={'quality': settings.CLIPBOARD_THUMBNAIL_QUALITY})

    filename = models.CharField(max_length=128, null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.file.name

    def get_thumbnail_url(self):
        if self.file:
            return self.image_thumbnail.url
