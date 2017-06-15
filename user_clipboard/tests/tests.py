import os
import shutil
from io import BytesIO
from datetime import timedelta
from PIL import Image

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.files.base import ContentFile, File
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.encoding import force_str

from user_clipboard.models import Clipboard
from user_clipboard.tests.models import ModelWithFile, ModelWithImage


class ClipboardTestMixin(object):

    def setUp(self):
        self.user1 = User.objects.create(username="user1", email='test@test.com')
        self.user1.set_password('1234')
        self.user1.save()

        with ContentFile('test file', 'test_file.txt') as test_file:
            self.fake_clipboard_file = Clipboard.objects.create(user=self.user1, file=test_file)

        with ContentFile('test file 2', 'test_file2.txt') as test_file2:
            self.fake_clipboard_file2 = Clipboard.objects.create(user=self.user1, file=test_file2)

        with BytesIO() as test_image:
            Image.new("RGBA", size=(50, 50), color=(256, 0, 0)).save(test_image, 'png')
            test_image.seek(0)
            self.fake_clipboard_image = Clipboard.objects.create(user=self.user1, file=File(test_image, 'test_image.png'))
            test_image.seek(0)
            self.fake_clipboard_image2 = Clipboard.objects.create(user=self.user1, file=File(test_image, 'test_image2.png'))

    def tearDown(self):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'clipboard'))
        cache_dir = os.path.join(settings.MEDIA_ROOT, 'CACHE')
        if os.path.isdir(cache_dir):
            shutil.rmtree(cache_dir)


class ClipboardTestApi(ClipboardTestMixin, TestCase):
    maxDiff = None

    def test_user1_not_authenticated_get(self):
        response = self.client.get(
            reverse('clipboard')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.get(
            reverse('clipboard', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(403, response.status_code)

        response = self.client.get(
            reverse('clipboard_images')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.get(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(403, response.status_code)

    def test_user1_not_authenticated_post(self):
        response = self.client.post(
            reverse('clipboard')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.post(
            reverse('clipboard', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(403, response.status_code)

        response = self.client.post(
            reverse('clipboard_images')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.post(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(403, response.status_code)

    def test_user1_not_authenticated_delete(self):
        response = self.client.delete(
            reverse('clipboard')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.delete(
            reverse('clipboard', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(403, response.status_code)

        response = self.client.delete(
            reverse('clipboard_images')
        )
        self.assertEqual(403, response.status_code)

        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(403, response.status_code)

    def test_user1_get_clipboard(self):
        self.client.login(username="user1", password=1234)
        clipboard_file = self.fake_clipboard_file
        clipboard_file2 = self.fake_clipboard_file2
        clipboard_image = self.fake_clipboard_image
        clipboard_image2 = self.fake_clipboard_image2

        response = self.client.get(
            reverse('clipboard')
        )
        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
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
                'thumbnail': clipboard_image.get_thumbnail_url(),
                'name': clipboard_image.filename,
            }, {
                'url': clipboard_image2.file.url,
                'id': clipboard_image2.pk,
                'thumbnail': clipboard_image2.get_thumbnail_url(),
                'name': clipboard_image2.filename,
            }]
        })

    def test_user1_get_clipboard_kwargs(self):
        self.client.login(username="user1", password=1234)
        clipboard_file = self.fake_clipboard_file

        response = self.client.get(
            reverse('clipboard', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk
            }
        })

    def test_user1_get_clipboard_images(self):
        self.client.login(username="user1", password=1234)
        clipboard_image = self.fake_clipboard_image
        clipboard_image2 = self.fake_clipboard_image2

        response = self.client.get(
            reverse('clipboard_images')
        )

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': [{
                'url': clipboard_image.file.url,
                'name': clipboard_image.filename,
                'thumbnail': clipboard_image.get_thumbnail_url(),
                'id': clipboard_image.pk
            }, {
                'url': clipboard_image2.file.url,
                'name': clipboard_image2.filename,
                'thumbnail': clipboard_image2.get_thumbnail_url(),
                'id': clipboard_image2.pk
            }]
        })

    def test_user1_get_clipboard_images_kwargs(self):
        self.client.login(username="user1", password=1234)
        clipboard_image = self.fake_clipboard_image

        response = self.client.get(
            reverse('clipboard_images', kwargs={'pk': clipboard_image.pk})
        )

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'url': clipboard_image.file.url,
                'name': clipboard_image.filename,
                'thumbnail': clipboard_image.get_thumbnail_url(),
                'id': clipboard_image.pk
            }
        })

    def test_file_clipboard_create_non_image_file(self):
        self.client.login(username="user1", password=1234)

        with ContentFile('test file', name='test_file.txt') as test_file:
            response = self.client.post(
                reverse('clipboard'),
                {'file': test_file}
            )

        clipboard_file = Clipboard.objects.latest('pk')

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk,
            }
        })

    def test_file_clipboard_create_image_file(self):
        self.client.login(username="user1", password=1234)

        with BytesIO() as test_image:
            Image.new("RGBA", size=(64, 64), color=(256, 128, 64)).save(test_image, 'png')
            test_image.seek(0)
            test_image.name = 'test_image.png'

            response = self.client.post(
                reverse('clipboard'), {'file': test_image}
            )

        clipboard_file = Clipboard.objects.latest('pk')

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'url': clipboard_file.file.url,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk,
                'thumbnail': clipboard_file.get_thumbnail_url(),
            }
        })

    def test_image_clipboard_create_non_image_file(self):
        self.client.login(username="user1", password=1234)

        with ContentFile('test file', name='test_file.txt') as test_file:
            response = self.client.post(
                reverse('clipboard_images'),
                {'file': test_file}
            )

        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'errors': {
                'file': ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']
            }
        })

    def test_image_clipboard_create_image_file(self):
        self.client.login(username="user1", password=1234)

        with BytesIO() as test_image:
            Image.new("RGBA", size=(64, 64), color=(256, 128, 64)).save(test_image, 'png')
            test_image.seek(0)
            test_image.name = 'test_image.png'

            response = self.client.post(
                reverse('clipboard_images'), {'file': test_image}
            )

        clipboard_file = Clipboard.objects.latest('pk')
        url_path = clipboard_file.file.url
        url_path_thumbnail = clipboard_file.get_thumbnail_url()

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'url': url_path,
                'name': clipboard_file.filename,
                'id': clipboard_file.pk,
                'thumbnail': url_path_thumbnail,
            }
        })

        if os.path.exists(settings.PROJECT_DIR + url_path):
            try:
                os.remove(settings.PROJECT_DIR + url_path)
                shutil.rmtree(os.path.abspath(os.path.join(settings.PROJECT_DIR + url_path_thumbnail, os.pardir)))
            except OSError as e:
                print(e)

    def test_file_clipboard_edit_file(self):
        self.client.login(username="user1", password=1234)
        with BytesIO() as test_image:
            Image.new("RGBA", size=(64, 64), color=(256, 128, 64)).save(test_image, 'png')
            test_image.seek(0)
            test_image.name = 'test_image.png'

            response = self.client.post(
                reverse('clipboard', kwargs={'pk': self.fake_clipboard_file.pk}),
                {'file': test_image}
            )

        file_for_edit = Clipboard.objects.get(pk=self.fake_clipboard_file.pk)

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'url': file_for_edit.file.url,
                'id': file_for_edit.pk,
                'thumbnail': file_for_edit.get_thumbnail_url(),
                'name': file_for_edit.filename
            }
        })

    def test_image_clipboard_edit_file(self):
        self.client.login(username="user1", password=1234)

        with ContentFile('test file', name='test_file.txt') as test_file:
            response = self.client.post(
                reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_image.pk}),
                {'file': test_file}
            )

        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'errors': {
                'file': ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']
            }
        })

    def test_404_image_clipboard_edit_file(self):
        self.client.login(username="user1", password=1234)

        with ContentFile('test file', name='test_file.txt') as test_file:
            response = self.client.post(
                reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_file.pk}),
                {'file': test_file}
            )

        self.assertEqual(404, response.status_code)

    def test_image_clipboard_edit_image(self):
        self.client.login(username="user1", password=1234)

        with BytesIO() as test_image:
            Image.new("RGBA", size=(64, 64), color=(256, 128, 64)).save(test_image, 'png')
            test_image.seek(0)
            test_image.name = 'test_image.png'

            response = self.client.post(
                reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_image.pk}),
                {'file': test_image}
            )

        image_for_edit = Clipboard.objects.get(pk=self.fake_clipboard_image.pk)

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'url': image_for_edit.file.url,
                'id': image_for_edit.pk,
                'thumbnail': image_for_edit.get_thumbnail_url(),
                'name': image_for_edit.filename,
            }
        })

    def test_clear_clipboard(self):
        self.client.login(username="user1", password=1234)
        self.assertTrue(Clipboard.objects.filter(user__username='user1').exists())

        response = self.client.delete(
            reverse('clipboard')
        )
        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'success': True
        })
        self.assertFalse(Clipboard.objects.filter(user__username='user1').exists())

    def test_delete_file_with_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'success': True
        })

    def test_delete_image_without_pk(self):
        self.client.login(username="user1", password=1234)
        self.assertTrue(Clipboard.objects.filter(user__username='user1', is_image=True).exists())
        response = self.client.delete(
            reverse('clipboard_images')
        )
        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'success': True
        })
        self.assertFalse(Clipboard.objects.filter(user__username='user1', is_image=True).exists())

    def test_delete_image_with_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_image.pk})
        )

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(force_str(response.content), {
            'success': True
        })

    def test_delete_404_image_with_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_image.pk})
        )

        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_image.pk})
        )

        self.assertEqual(404, response.status_code)

    def test_delete_404_file_with_pk(self):
        self.client.login(username="user1", password=1234)
        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        response = self.client.delete(
            reverse('clipboard_images', kwargs={'pk': self.fake_clipboard_file.pk})
        )

        self.assertEqual(404, response.status_code)

    def test_delete_expired(self):
        with ContentFile('Active File', name='active.txt') as active_file:
            active = Clipboard.objects.create(
                file=active_file,
                user=self.user1,
            )
        with ContentFile('Expired File', name='expired.txt') as expired_file:
            expired = Clipboard.objects.create(
                file=expired_file,
                user=self.user1,
                date_created=timezone.now() - timedelta(days=30)
            )

        call_command('clear_clipboard')

        self.assertTrue(Clipboard.objects.filter(pk=active.pk).exists())
        self.assertFalse(Clipboard.objects.filter(pk=expired.pk).exists())


@override_settings(ROOT_URLCONF='user_clipboard.tests.urls')
class ClipboardUsageTest(ClipboardTestMixin, TestCase):

    def tearDown(self):
        super(ClipboardUsageTest, self).tearDown()
        try:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'documents'))
        except OSError:
            pass
        try:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'images'))
        except OSError:
            pass

    def test_use_clipboard_file(self):
        self.client.login(username='user1', password='1234')

        response = self.client.post(
            reverse('test_user_clipboard_upload_document'),
            data={
                'document': self.fake_clipboard_file.pk,
            },
        )
        self.assertEqual(response.status_code, 200)

        instance = ModelWithFile.objects.latest('pk')
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'pk': instance.pk,
                'document': '/media/documents/test_file.txt',
            }
        })

    def test_use_clipboard_image(self):
        self.client.login(username='user1', password='1234')

        response = self.client.post(
            reverse('test_user_clipboard_upload_image'),
            data={
                'image': self.fake_clipboard_image.pk,
            },
        )
        self.assertEqual(response.status_code, 200)

        instance = ModelWithImage.objects.latest('pk')
        self.assertJSONEqual(force_str(response.content), {
            'data': {
                'pk': instance.pk,
                'image': '/media/images/test_image.png',
            }
        })
