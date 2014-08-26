import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

THUMBNAIL_WIDTH = getattr(settings, 'CLIPBOARD_IMAGE_WIDTH', 100)
THUMBNAIL_HEIGHT = getattr(settings, 'CLIPBOARD_IMAGE_HEIGHT', 100)
THUMBNAIL_QUALITY = getattr(settings, 'CLIPBOARD_THUMBNAIL_QUALITY', 80)


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
                                     processors=[ResizeToFill(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)],
                                     format='JPEG',
                                     options={'quality': THUMBNAIL_QUALITY})

    filename = models.CharField(max_length=128, null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.file.name

    def get_thumbnail_url(self):
        if self.file:
            return self.image_thumbnail.url
