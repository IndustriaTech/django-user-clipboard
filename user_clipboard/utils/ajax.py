try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.http import HttpResponse
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

JSON_CONTENT_TYPE = 'application/json; charset=%s' % (settings.DEFAULT_CHARSET, )
JSON_FALLBACK_CONTENT_TYPE = "text/plain; charset=%s" % (settings.DEFAULT_CHARSET, )


class JSONResponse(HttpResponse):
    """
    Response that will return JSON serialized value of the content.

    It accept request as first argument because it needs to set correct
    content type for older versions of IE.

    """
    INDENT = 1 if settings.DEBUG else None

    def __init__(self, request, content, *args, **kwargs):

        accept = request.META.get('HTTP_ACCEPT', '*/*')
        if 'text/html' in accept and 'application/json' not in accept:
            content_type = JSON_FALLBACK_CONTENT_TYPE
        else:
            content_type = JSON_CONTENT_TYPE

        json_content = json.dumps(content, cls=DjangoJSONEncoder, indent=self.INDENT)

        super(JSONResponse, self).__init__(json_content, content_type, *args, **kwargs)
