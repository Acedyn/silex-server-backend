from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from api.models import Project, Sequence, Shot


class AuthentificatedTestBase(TestCase):
    def setUp(self) -> None:
        # Create users
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            username="test", email="test@silex.com"
        )
        self.user.save()
        self.dummy_user = get_user_model().objects.create(
            username="dummy", email="dummy@silex.com"
        )
        self.dummy_user.save()
        # Connect user
        self.client.force_authenticate(self.user)

        # Create dummy project
        project_data = {
            "root": "/tars/test_pipe",
            "framerate": 24.975,
            "width": 4096,
            "height": 2160,
            "label": "TEST PIPE",
            "name": "test-pipe",
            "created_by": self.user,
        }
        self.dummy_project = Project.objects.create(**project_data)
        self.dummy_project.save()
        self.assertEqual(Project.objects.count(), 1)

        # Create dummy sequence
        sequence_data = {
            "root": "/seq010",
            "framerate": self.dummy_project.framerate,
            "index": 10,
            "width": 4096,
            "height": 2160,
            "project": self.dummy_project,
            "created_by": self.user,
        }
        self.dummy_sequence = Sequence.objects.create(**sequence_data)
        self.dummy_sequence.save()
        self.assertEqual(Sequence.objects.count(), 1)

        # Create dummy shot
        shot_data = {
            "root": "/sh010",
            "framerate": self.dummy_sequence.framerate,
            "index": 10,
            "width": 4096,
            "height": 2160,
            "sequence": self.dummy_sequence,
            "created_by": self.user,
        }
        self.dummy_shot = Shot.objects.create(**shot_data)
        self.dummy_shot.save()
        self.assertEqual(Shot.objects.count(), 1)
