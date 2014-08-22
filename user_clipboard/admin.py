from django.contrib import admin
from .models import Clipboard
# Register your models here.


class ClipboardAdmin(admin.ModelAdmin):

    list_display = 'filename', 'user', 'file',
    readonly_fields = 'filename', 'thumbnail',

admin.site.register(Clipboard, ClipboardAdmin)
