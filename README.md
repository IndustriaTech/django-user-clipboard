# Django User Clipboard

This app returns to user JSONs from uploaded file/image.

This app is **IS** connected with django user model.

This app needs:
	- easy_thumbnails

## SetUp

Install the app:

    pip install ....

You should have these in installed apps:

    INSTALLED_APPS = (
        ....

        'easy_thumbnails',
    	'user_clipboard',
    )

Add the urls in your main urls.py file:

    url(r'^clipboard/', include('user_clipboard.urls')),

Run migrations or syncdb depending on whether you use South.