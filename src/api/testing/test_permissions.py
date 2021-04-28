from rest_framework import status
from api.models import Sequence, Shot
from api.testing.test_base import AuthentificatedTestBase


class PermissionsTestCase(AuthentificatedTestBase):
    def test_create_unauthorized_sequence(self):
        print("\nTesting : Create unauthorized sequence ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)

        data = {
            "root": "/seq020",
            "index": 20,
            "width": 4096,
            "height": 2160,
            "project": f"http://testserver/projects/{self.dummy_project.id}/",
        }
        response = self.client.post("/sequences/", data, format="json")
        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Test the stored values
        self.assertEqual(Sequence.objects.count(), 1)

    def test_create_authorized_sequence(self):
        print("\nTesting : Create unauthorized shot ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Add dummy_project to dummy_user's projects
        self.dummy_user.projects.set(
            [
                self.dummy_project,
            ]
        )
        self.dummy_user.save()

        data = {
            "root": "/seq020",
            "index": 20,
            "width": 4096,
            "height": 2160,
            "project": f"http://testserver/projects/{self.dummy_project.id}/",
        }
        response = self.client.post("/sequences/", data, format="json")
        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test the stored values
        self.assertEqual(Sequence.objects.count(), 2)

    def test_create_unauthorized_shot(self):
        print("\nTesting : Create unauthorized shot ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)

        data = {
            "root": "/sh030",
            "index": 30,
            "width": 4096,
            "height": 2160,
            "sequence": f"http://testserver/sequences/{self.dummy_sequence.id}/",
        }
        response = self.client.post("/shots/", data, format="json")
        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Test the stored values
        self.assertEqual(Shot.objects.count(), 1)

    def test_create_authorized_shot(self):
        print("\nTesting : Create unauthorized shot ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Add dummy_project to dummy_user's projects
        self.dummy_user.projects.set(
            [
                self.dummy_project,
            ]
        )
        self.dummy_user.save()

        data = {
            "root": "/sh030",
            "index": 30,
            "width": 4096,
            "height": 2160,
            "sequence": f"http://testserver/sequences/{self.dummy_sequence.id}/",
        }
        response = self.client.post("/shots/", data, format="json")
        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test the stored values
        self.assertEqual(Shot.objects.count(), 2)
