from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, UserDetails

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890'
        }
        self.user_details_data = {
            'age': 25,
            'address': '123 Test St',
            'date_of_birth': '1990-01-01',
            'hobby': 'Reading',
            'profession': 'Engineer'
        }

    def test_signup(self):
        url = reverse('signup')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_login(self):
        user = User.objects.create_user(**self.user_data)
        url = reverse('login')
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_details(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        url = reverse('user-details')
        response = self.client.post(url, self.user_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserDetails.objects.count(), 1)
        self.assertEqual(UserDetails.objects.get().user, user)

    def test_update_profile(self):
        user = User.objects.create_user(**self.user_data)
        user_details = UserDetails.objects.create(user=user, **self.user_details_data)
        self.client.force_authenticate(user=user)
        url = reverse('update-profile', kwargs={'pk': user_details.pk})
        updated_data = {'age': 30, 'address': '456 Updated St'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_details.refresh_from_db()
        self.assertEqual(user_details.age, 30)
        self.assertEqual(user_details.address, '456 Updated St')

    def test_delete_user(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        url = reverse('delete-user', kwargs={'pk': user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)