import os
import json

from urllib import urlencode

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File as DJ
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client as DJClient

from .models import Clipboard

REQUEST_CONTENT = 'application/x-www-form-urlencoded'


class Client(DJClient):

    def delete(self, path, data={}, content_type=REQUEST_CONTENT,
            follow=False, **extra):
        """
        Send a resource to the server using DELETE.
        """
        put_data = urlencode(data) if content_type.startswith(REQUEST_CONTENT) else data
        response = super(Client, self).delete(path,
                data=put_data, content_type=content_type, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response


class ClipboardTestMixin(object):
    client_class = Client

    def setUp(self):
        self.user1 = User.objects.create(username="user1", email='test@test.com')
        self.user1.set_password('1234')
        self.user1.save()

        self.file_path_test = os.path.abspath('../user_clipboard/test_file.txt')
        self.image_path_test = os.path.abspath('../user_clipboard/test_image.jpg')

        self.file_test = open(self.file_path_test, 'r')
        self.image_test = open(self.image_path_test, 'r')

        self.fake_clipboard_file = Clipboard.objects.create(user=self.user1, file=DJ(self.file_test, 'test_file.txt'))
        self.fake_clipboard_file.save()
        self.fake_clipboard_file2 = Clipboard.objects.create(user=self.user1, file=DJ(self.file_test, 'test_file2.txt'))
        self.fake_clipboard_file2.save()

        self.fake_clipboard_image = Clipboard.objects.create(user=self.user1, file=DJ(self.image_test, 'test_image.jpg'))
        self.fake_clipboard_image.thumbnail = self.fake_clipboard_image.get_thumbnail_url()
        self.fake_clipboard_image.save()
        self.fake_clipboard_image2 = Clipboard.objects.create(user=self.user1, file=DJ(self.image_test, 'test_image2.jpg'))
        self.fake_clipboard_image2.thumbnail = self.fake_clipboard_image2.get_thumbnail_url()
        self.fake_clipboard_image2.save()

    def tearDown(self):
        url_file_path = self.fake_clipboard_file.file.url
        url_file_path2 = self.fake_clipboard_file2.file.url
        url_image_path = self.fake_clipboard_image.file.url
        url_thumbnail_path = self.fake_clipboard_image.thumbnail
        url_image_path2 = self.fake_clipboard_image2.file.url
        url_thumbnail_path2 = self.fake_clipboard_image2.thumbnail

        if os.path.exists(settings.PROJECT_DIR + url_file_path):
            try:
                os.remove(settings.PROJECT_DIR + url_file_path)
                os.remove(settings.PROJECT_DIR + url_file_path2)
            except OSError as e:
                print e

        if os.path.exists(settings.PROJECT_DIR + url_image_path):
            try:
                os.remove(settings.PROJECT_DIR + url_image_path)
                os.remove(settings.PROJECT_DIR + url_thumbnail_path)
                os.remove(settings.PROJECT_DIR + url_image_path2)
                os.remove(settings.PROJECT_DIR + url_thumbnail_path2)
            except OSError as e:
                print e


class ClipboardTestApi(ClipboardTestMixin, TestCase):
    maxDiff = None

    def test_user1_not_authenticated_get(self):
        response = self.client.get(
            reverse('clipboard')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.get(
            reverse('clipboard', kwargs={'pk': 1})
        )

        self.assertEqual(403, response.status_code)

        response = self.client.get(
            reverse('clipboard_images')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.get(
            reverse('clipboard_images', kwargs={'pk': 1})
        )

        self.assertEqual(403, response.status_code)

    def test_user1_not_authenticated_post(self):
        response = self.client.post(
            reverse('clipboard')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.post(
            reverse('clipboard', kwargs={'pk': 1})
        )

        self.assertEqual(403, response.status_code)

        response = self.client.post(
            reverse('clipboard_images')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.post(
            reverse('clipboard_images', kwargs={'pk': 1})
        )

        self.assertEqual(403, response.status_code)

    def test_user1_not_authenticated_delete(self):
        response = self.client.delete(
            reverse('clipboard')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.delete(
            reverse('clipboard', kwargs={'pk': 1})
        )

        self.assertEqual(403, response.status_code)

        response = self.client.delete(
            reverse('clipboard_images')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': 1})
        )

        self.assertEqual(403, response.status_code)

    def test_user1_get_clipboard(self):
        self.client.login(username="user1", password=1234)
        clipboard_file = Clipboard.objects.get(user=self.user1, pk=1)
        clipboard_file2 = Clipboard.objects.get(user=self.user1, pk=2)
        clipboard_image = Clipboard.objects.get(user=self.user1, pk=3)
        clipboard_image2 = Clipboard.objects.get(user=self.user1, pk=4)

        response = self.client.get(
            reverse('clipboard')
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertDictEqual(data, {
            'data': [{
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk
            }, {
                'url': clipboard_file2.file.url,
                'name': clipboard_file2.filename,
                'id': clipboard_file2.pk
            }, {
                'url': clipboard_image.file.url,
                'id': clipboard_image.pk,
                'thumbnail': clipboard_image.thumbnail,
                'name': clipboard_image.filename,
            }, {
                'url': clipboard_image2.file.url,
                'id': clipboard_image2.pk,
                'thumbnail': clipboard_image2.thumbnail,
                'name': clipboard_image2.filename,
            }]
        })

    def test_user1_get_clipboard_kwargs(self):
        self.client.login(username="user1", password=1234)
        clipboard_file = Clipboard.objects.get(user=self.user1, pk=1)

        response = self.client.get(
            reverse('clipboard', kwargs={'pk': 1})
        )

        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertDictEqual(data, {
            'data': [{
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk
            }]
        })

    def test_user1_get_clipboard_images(self):
        self.client.login(username="user1", password=1234)
        clipboard_image = Clipboard.objects.get(user=self.user1, pk=3)
        clipboard_image2 = Clipboard.objects.get(user=self.user1, pk=4)

        response = self.client.get(
            reverse('clipboard_images')
        )

        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertDictEqual(data, {
            'data': [{
                'url': clipboard_image.file.url,
                'name': clipboard_image.filename,
                'thumbnail': clipboard_image.thumbnail,
                'id': clipboard_image.pk
            },{
                'url': clipboard_image2.file.url,
                'name': clipboard_image2.filename,
                'thumbnail': clipboard_image2.thumbnail,
                'id': clipboard_image2.pk
            }]
        })

    def test_user1_get_clipboard_images_kwargs(self):
        self.client.login(username="user1", password=1234)
        clipboard_image = Clipboard.objects.get(user=self.user1, pk=3)

        response = self.client.get(
            reverse('clipboard_images', kwargs={'pk': 3})
        )

        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertDictEqual(data, {
            'data': [{
                'url': clipboard_image.file.url,
                'name': clipboard_image.filename,
                'thumbnail': clipboard_image.thumbnail,
                'id': clipboard_image.pk
            }]
        })

    def test_file_clipboard_create_non_image_file(self):
        self.client.login(username="user1", password=1234)
        file_path = os.path.abspath('../user_clipboard/test_file.txt')
        f = open(file_path, 'r')
        post_data = {}
        post_data['file'] = f
        response = self.client.post(
            reverse('clipboard'), post_data
        )

        data = json.loads(response.content)

        url_path = data['data']['url']
        clipboard_file = Clipboard.objects.get(pk=5)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(data, {
            'data': {
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk,
            }
        })

        if os.path.exists(settings.PROJECT_DIR + url_path):
            try:
                os.remove(settings.PROJECT_DIR + url_path)
            except OSError as e:
                print e

    def test_file_clipboard_create_image_file(self):
        self.client.login(username="user1", password=1234)
        file_path = os.path.abspath('../user_clipboard/test_image.jpg')

        f = open(file_path, 'r')
        post_data = {}

        post_data['file'] = f
        response = self.client.post(
            reverse('clipboard'), post_data
        )

        data = json.loads(response.content)

        url_path = data['data']['url']
        url_path_thumbnail = data['data']['thumbnail']
        clipboard_file = Clipboard.objects.get(pk=5)

        self.assertEqual(200, response.status_code)
        self.assertDictEqual(data, {
            'data': {
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk,
                'thumbnail': clipboard_file.thumbnail,
            }
        })

        if os.path.exists(settings.PROJECT_DIR + url_path):
            try:
                os.remove(settings.PROJECT_DIR + url_path)
                os.remove(settings.PROJECT_DIR + url_path_thumbnail)
            except OSError as e:
                print e

    def test_image_clipboard_create_non_image_file(self):
            self.client.login(username="user1", password=1234)
            file_path = os.path.abspath('../user_clipboard/test_file.txt')
            f = open(file_path, 'r')
            post_data = {}
            post_data['file'] = f
            response = self.client.post(
                reverse('clipboard_images'), post_data
            )

            self.assertEqual(200, response.status_code)

            data = json.loads(response.content)

            self.assertDictEqual(data, {
                'errors': {
                    'file': ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']
                }
            })

    def test_image_clipboard_create_image_file(self):
        self.client.login(username="user1", password=1234)
        file_path = os.path.abspath('../user_clipboard/test_image.jpg')

        f = open(file_path, 'r')
        post_data = {}

        post_data['file'] = f
        response = self.client.post(
            reverse('clipboard_images'), post_data
        )

        data = json.loads(response.content)

        url_path = data['data']['url']
        url_path_thumbnail = data['data']['thumbnail']
        clipboard_file = Clipboard.objects.get(pk=5)

        self.assertEqual(200, response.status_code)
        self.assertDictEqual(data, {
            'data': {
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk,
                'thumbnail': clipboard_file.thumbnail,
            }
        })

        if os.path.exists(settings.PROJECT_DIR + url_path):
            try:
                os.remove(settings.PROJECT_DIR + url_path)
                os.remove(settings.PROJECT_DIR + url_path_thumbnail)
            except OSError as e:
                print e

    def test_file_clipboard_edit_file(self):
        self.client.login(username="user1", password=1234)
        file_path = os.path.abspath('../user_clipboard/test_image_edit.jpg')

        f = open(file_path, 'r')
        post_data = {}

        post_data['file'] = f

        response = self.client.post(
            reverse('clipboard', kwargs={'pk': 1}), post_data
        )

        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)

        url_path = data['data']['url']
        url_path_thumbnail = data['data']['thumbnail']
        file_for_edit = Clipboard.objects.get(pk=1)

        self.assertDictEqual(data, {
            'data': {
                'url': file_for_edit.file.url,
                'id': file_for_edit.pk,
                'thumbnail': file_for_edit.thumbnail,
                'name': file_for_edit.filename
            }
        })

        if os.path.exists(settings.PROJECT_DIR + url_path):
            try:
                os.remove(settings.PROJECT_DIR + url_path)
                os.remove(settings.PROJECT_DIR + url_path_thumbnail)
            except OSError as e:
                print e

    def test_image_clipboard_edit_file(self):
        self.client.login(username="user1", password=1234)
        file_path = os.path.abspath('../user_clipboard/test_file.txt')

        f = open(file_path, 'r')
        post_data = {}

        post_data['file'] = f

        response = self.client.post(
            reverse('clipboard_images', kwargs={'pk': 1}), post_data
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)

        self.assertDictEqual(data, {
            'errors': {
                'file': ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']
            }
        })

    def test_image_clipboard_edit_image(self):
        self.client.login(username="user1", password=1234)
        file_path = os.path.abspath('../user_clipboard/test_image_edit.jpg')

        f = open(file_path, 'r')
        post_data = {}

        post_data['file'] = f

        response = self.client.post(
            reverse('clipboard_images', kwargs={'pk': 3}), post_data
        )

        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        url_path = data['data']['url']
        url_path_thumbnail = data['data']['thumbnail']
        image_for_edit = Clipboard.objects.get(pk=3)

        self.assertDictEqual(data, {
            'data': {
                'url': image_for_edit.file.url,
                'id': image_for_edit.pk,
                'thumbnail': image_for_edit.thumbnail,
                'name': image_for_edit.filename,
            }
        })

        if os.path.exists(settings.PROJECT_DIR + url_path):
            try:
                os.remove(settings.PROJECT_DIR + url_path)
                os.remove(settings.PROJECT_DIR + url_path_thumbnail)
            except OSError as e:
                print e

    def test_delete_file_without_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard')
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)

        self.assertDictEqual(data, {
            'error': 'Need a pk for delete'
        })

    def test_delete_file_with_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard', kwargs={'pk': 1})
        )

        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)

        self.assertDictEqual(data, {
            'success': True
        })

    def test_delete_image_without_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard_images')
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)

        self.assertDictEqual(data, {
            'error': 'Need a pk for delete'
        })

    def test_delete_image_with_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': 3})
        )

        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)

        self.assertDictEqual(data, {
            'success': True
        })
