from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'rt') as readme:
    README = readme.read()

setup(
    name='django-user-clipboard',
    version='0.6.2',
    url='https://github.com/IndustriaTech/django-user-clipboard',
    description='Clipboard API',
    author='Vladimir Rusinov',
    author_email='vladimirrussinov@gmail.com',
    maintainer='Venelin Stoykov',
    maintainer_email='venelin.stoykov@industria.tech',
    long_description=README,
    install_requires=[
        'Pillow',
        'django-imagekit',
    ],
    packages=[
        'user_clipboard',
        'user_clipboard.management',
        'user_clipboard.management.commands',
        'user_clipboard.migrations',
        'user_clipboard.south_migrations',
        'user_clipboard.utils',
    ],
    package_data={
        '': ['LICENSE', 'README.rst']
    },
    include_package_data=True,
    zip_safe=False,
    keywords=['Clipboard', 'Clipboard API', 'File Clipboard', 'Image Clipboard'],
    license='The MIT License (MIT)',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP/JSON',
    ],
)
