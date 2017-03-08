from django.core.management.base import BaseCommand

from user_clipboard.models import Clipboard


class Command(BaseCommand):
    help = "Clear old clipboard items"

    def handle(self, *args, **options):
        Clipboard.objects.expired().delete()
