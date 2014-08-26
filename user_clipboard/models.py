import uuid

from PIL import Image

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
    filename = models.CharField(max_length=128, null=True, blank=True)
    is_image = models.BooleanField(editable=False, default=False)

    image_thumbnail = ImageSpecField(source='file',
                                     processors=[ResizeToFill(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)],
                                     format='JPEG',
                                     options={'quality': THUMBNAIL_QUALITY})

    def __unicode__(self):
        return self.filename

    def save(self, *args, **kwargs):
        if self.file is not None and not self.file._committed:
            # We have new file then check if it is and image or not.
            if hasattr(self.file, 'content_type'):
                self.is_image = self.file.content_type.startswith('image')
            else:
                try:
                    Image.open(self.file).verify()
                except:
                    self.is_image = False
                else:
                    self.is_image = True
                finally:
                    self.file.seek(0)
        super(Clipboard, self).save(*args, **kwargs)

    def get_thumbnail_url(self):
        if self.is_image and self.file:
            return self.image_thumbnail.url
