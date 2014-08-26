# Django User Clipboard

This app returns to user JSONs from uploaded file/image.

This app is **IS** connected with django user model.

This app needs:
	- django-imagekit

## SetUp

Install the app:

    pip install ....

You should have these in installed apps:

    INSTALLED_APPS = (
        ....

        'imagekit',
    	'user_clipboard',
    )

Add the urls in your main urls.py file:

    url(r'^clipboard/', include('user_clipboard.urls')),

You can configure defaut values with theese settings:

	CLIPBOARD_IMAGE_WIDTH = 100
	CLIPBOARD_IMAGE_HEIGHT = 100
	CLIPBOARD_THUMBNAIL_QUALITY = 80

Run migrations or syncdb depending on whether you use South.
