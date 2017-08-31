Django User Clipboard
=====================

This app returns to user JSONs from uploaded file/image.

This app is connected with django user model.

This app needs :code:`django-imagekit`

SetUp
-----

Install the app:
::

    pip install git+https://github.com/IndustriaTech/django-user-clipboard.git

You should have these in installed apps:
::

    INSTALLED_APPS = (
        ....

        'imagekit',
    	'user_clipboard',
    )

Add the urls in your main :code:`urls.py` file:
::

    url(r'^clipboard/', include('user_clipboard.urls')),

You can configure defaut values with theese settings:
::

	CLIPBOARD_IMAGE_WIDTH = 100
	CLIPBOARD_IMAGE_HEIGHT = 100
	CLIPBOARD_THUMBNAIL_QUALITY = 80

And finally you can run the migrations:
::

    python manage.py migrate

In order to clear old objects from the storage you need to periodically clear the storage.
You can achieve that by executing:
::

    python manage.py clear_clipboard

By default all files older than one hour are deleted. You can configure the time by setting:
::

    CLIPBOARD_EXPIRATION_TIME = 60 * 60

Programatically you can delete these in your python code by calling:
::

    Clipboard.objects.expired().delete()

You need to configre cron or celery or something else to clear the storage periodically.
