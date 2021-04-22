from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate, APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from api.models import Project

class ProjectTests(APITestCase):
    def setUp(self):
        self.user = User.objects.get(username='simon')
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_create_project(self):
        # Ensure we can create a new account object.
        data = {'root': '/tars/project', 'framerate': 24.5, 'width': 4096, 'height': 1080, 'label': 'TEST PIPE'}
        response = self.client.post('/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'test-pipe')
