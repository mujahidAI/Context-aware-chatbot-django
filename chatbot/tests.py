from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserAPIKey
from .services import encrypt_api_key, decrypt_api_key

class UserAPIKeyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = '/api/user-api-key/'

    def test_create_api_key(self):
        data = {'api_key': 'my-secret-key'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserAPIKey.objects.filter(user=self.user).exists())

        user_key = UserAPIKey.objects.get(user=self.user)
        self.assertEqual(decrypt_api_key(user_key.encrypted_key), 'my-secret-key')

    def test_get_api_key_status(self):
        UserAPIKey.objects.create(
            user=self.user,
            encrypted_key=encrypt_api_key('my-secret-key'),
            selected_model='llama-3.3-70b-versatile'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['selected_model'], 'llama-3.3-70b-versatile')
        self.assertNotIn('api_key', response.data) # Should not expose key

    def test_update_model_without_key(self):
        UserAPIKey.objects.create(
            user=self.user,
            encrypted_key=encrypt_api_key('old-key'),
            selected_model='old-model'
        )
        data = {'selected_model': 'new-model'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_key = UserAPIKey.objects.get(user=self.user)
        self.assertEqual(user_key.selected_model, 'new-model')
        self.assertEqual(decrypt_api_key(user_key.encrypted_key), 'old-key') # Key should remain

    def test_delete_api_key(self):
        UserAPIKey.objects.create(
            user=self.user,
            encrypted_key=encrypt_api_key('key'),
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserAPIKey.objects.filter(user=self.user).exists())
