from urllib import urlencode

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client as DJClient
# Create your tests here.
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

class ClipboardTestApi(ClipboardTestMixin, TestCase):

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


    def test_user1_get(self):
        self.client.login(username="user1", password=1234)

        response = self.client.get(
            reverse('clipboard')
        )
        self.assertEqual(200, response.status_code)

        response = self.client.get(
            reverse('clipboard', kwargs={'pk': 1})
        )

        self.assertEqual(200, response.status_code)

        response = self.client.get(
            reverse('clipboard_images')
        )
        self.assertEqual(200, response.status_code)

        response = self.client.get(
            reverse('clipboard_images', kwargs={'pk': 1})
        )

        self.assertEqual(200, response.status_code)


