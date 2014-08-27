from django.core.management.base import NoArgsCommand

from user_clipboard.models import Clipboard


class Command(NoArgsCommand):
    help = "Clear old clipboard items"

    def handle_noargs(self, **options):
        Clipboard.objects.expired().delete()
