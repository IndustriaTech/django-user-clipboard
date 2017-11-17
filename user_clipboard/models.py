import uuid

from PIL import Image
from datetime import timedelta

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.functional import cached_property

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .files import ClipboardFile, ClipboardImageFile

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


class ClipboardManager(models.Manager):
    def expired(self):
        expiration_time = getattr(settings, 'CLIPBOARD_EXPIRATION_TIME', 60 * 60)
        return self.filter(date_created__lt=timezone.now() - timedelta(seconds=expiration_time))


class Clipboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=new_file_upload_to, max_length=128)
    filename = models.CharField(max_length=256, editable=False, default='')
    is_image = models.BooleanField(editable=False, default=False, db_index=True)
    date_created = models.DateTimeField(editable=False, default=timezone.now, db_index=True)

    image_thumbnail = ImageSpecField(source='file',
                                     processors=[ResizeToFill(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)],
                                     format='JPEG',
                                     options={'quality': THUMBNAIL_QUALITY})

    objects = ClipboardManager()

    class Meta:
        verbose_name = 'Clipboard Item'
        verbose_name_plural = 'Clipboard'

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
            # Work around bug in django-imagekit (https://github.com/matthewwithanm/django-imagekit/issues/429)
            closed = self.file.closed
            try:
                return self.image_thumbnail.url
            finally:
                if closed:
                    self.file.close()

    @property
    def thumbnail(self):
        if self.is_image:
            return self.image_thumbnail

    @cached_property
    def uploaded_file(self):
        return self.get_file()

    @cached_property
    def uploaded_image(self):
        return self.get_image()

    def get_file(self):
        """
        Method that returns File object ready to be assigned to FileField.
        It replaces UploadedFile.
        """
        return ClipboardFile(self.file, self.filename)

    def get_image(self):
        """
        Method that returns ImageFile object ready to be assigned to ImageField.
        It replaces UploadedFile.
        """
        if self.is_image:
            return ClipboardImageFile(self.file, self.filename)


@receiver(post_delete, sender=Clipboard)
def _handle_deleteing(sender, instance, **kwargs):
    """
    Delete file when Clipboard item was deleted
    """
    if instance.file:
        instance.file.delete(save=False)
