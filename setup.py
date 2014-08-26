from setuptools import setup
import os

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-user-clipboard',
    url='',
    version='0.1',
    description='Clipboard API',
    author='Vladimir Rusinov',
    author_email='vladimirrussinov@gmail.com',
    long_description=README,
    install_requires=[
        'easy-thumbnails>=2.1'
    ],
    packages=[
        'user_clipboard',
        'user_clipboard.migrations',
        'user_clipboard.utils',
        'user_clipboard.tests_files'
    ],
    package_data={'': ['license.txt']},
    include_package_data=True,
    keywords=['Clipboard', 'Clipboard API', 'File Clipboard', 'Image Clipboard'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP/JSON',
    ],
)
