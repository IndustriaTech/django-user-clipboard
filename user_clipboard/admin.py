from django.contrib import admin
from imagekit.admin import AdminThumbnail
from .models import Clipboard


class ClipboardAdmin(admin.ModelAdmin):
    _thumbnail = AdminThumbnail(image_field='thumbnail')

    list_display = 'filename', 'user', '_thumbnail', 'date_created',
    readonly_fields = 'filename', '_thumbnail', 'date_created',

admin.site.register(Clipboard, ClipboardAdmin)
