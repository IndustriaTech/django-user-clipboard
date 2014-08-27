from django.contrib import admin
from imagekit.admin import AdminThumbnail
from .models import Clipboard


class ClipboardAdmin(admin.ModelAdmin):
    _thumbnail = AdminThumbnail(image_field='thumbnail')

    list_display = 'filename', 'user', '_thumbnail',
    readonly_fields = 'filename', '_thumbnail',

admin.site.register(Clipboard, ClipboardAdmin)
