from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.models import Project, Sequence


class AuthentificatedTestBase(TestCase):
    def setUp(self) -> None:
        # Connect user
        self.client = APIClient()
        self.user = User.objects.create(username="test")
        self.user.save()
        self.client.force_authenticate(self.user)

        # Create dummy project
        project_data = {
            "root": "/tars/test_pipe",
            "framerate": 24.975,
            "width": 4096,
            "height": 2160,
            "label": "TEST PIPE",
            "name": "test-pipe",
        }
        self.dummy_project = Project.objects.create(**project_data)
        self.dummy_project.save()
        self.assertEqual(Project.objects.count(), 1)

        # Create dummy sequence
        sequence_data = {
            "root": "/tars/test_pipe/seq010",
            "index": 10,
            "width": 4096,
            "height": 2160,
            "project": self.dummy_project,
        }
        self.dummy_sequence = Sequence.objects.create(**sequence_data)
        self.dummy_sequence.save()
        self.assertEqual(Sequence.objects.count(), 1)
