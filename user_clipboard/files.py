from django.core.files import File
from django.core.files.images import ImageFile


class ClipboardFile(File):
    """File that will be used instead of uploaded file"""

    def open(self, mode='rb'):
        # Django normal files try to open from filesystem but ClipboardFile
        # will be initialyzed with FieldFile which nows how to reopen itself
        # from configured storage
        self.file.open(mode=mode)
        return self


class ClipboardImageFile(ImageFile, ClipboardFile):
    """File that will be used instead of uploaded file but for images"""
    pass
