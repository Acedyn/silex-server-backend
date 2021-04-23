from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.models import Project

class AuthentificatedTestBase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username="test")
        self.user.save()
        self.client.force_authenticate(self.user)

        self.dummy_project = Project.objects.create(root='/tars/test_pipe', framerate=24.975, width=4096, height=2160, label='TEST PIPE')
        self.dummy_project.save()
