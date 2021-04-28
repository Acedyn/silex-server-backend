from django.contrib.auth.models import Group
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

    def test_update_unauthorized_sequence(self):
        print("\nTesting : update unauthorized sequence ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)

        # Get the already existing sequence, created in test_base.py
        get_response = self.client.get("/sequences/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/seq020",
        }
        sequence_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(sequence_url, data, format="json")

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        # Test the stored values
        self.dummy_sequence.refresh_from_db()
        self.assertEqual(self.dummy_sequence.root, "/seq010")

    def test_update_authorized_sequence(self):
        print("\nTesting : update unauthorized sequence ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Add dummy_project to dummy_user's projects
        self.dummy_user.projects.set(
            [
                self.dummy_project,
            ]
        )
        self.dummy_user.save()

        # Get the already existing sequence, created in test_base.py
        get_response = self.client.get("/sequences/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/seq020",
        }
        sequence_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(sequence_url, data, format="json")

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Test the stored values
        self.dummy_sequence.refresh_from_db()
        self.assertEqual(self.dummy_sequence.root, "/seq020")

    def test_create_sequence_elevated_permission(self):
        print("\nTesting : Create shot with elevated permissions ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Attach the user to the developper_group so he gets all right
        developper_group = Group.objects.get(name="developper")
        self.dummy_user.groups.add(developper_group)
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

    def test_update_sequence_elevated_permission(self):
        print("\nTesting : Create shot with elevated permissions ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Attach the user to the developper_group so he gets all right
        developper_group = Group.objects.get(name="developper")
        self.dummy_user.groups.add(developper_group)
        self.dummy_user.save()

        # Get the already existing sequence, created in test_base.py
        get_response = self.client.get("/sequences/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/seq020",
        }
        sequence_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(sequence_url, data, format="json")

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Test the stored values
        self.dummy_sequence.refresh_from_db()
        self.assertEqual(self.dummy_sequence.root, "/seq020")

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

    def test_update_unauthorized_shot(self):
        print("\nTesting : Update unauthorized shot ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)

        # Get the already existing shot, created in test_base.py
        get_response = self.client.get("/shots/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/sh30",
        }
        shot_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(shot_url, data, format="json")

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        # Test the stored values
        self.dummy_shot.refresh_from_db()
        self.assertEqual(self.dummy_shot.root, "/sh020")

    def test_update_authorized_shot(self):
        print("\nTesting : Update unauthorized shot ")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Add dummy_project to dummy_user's projects
        self.dummy_user.projects.set(
            [
                self.dummy_project,
            ]
        )
        self.dummy_user.save()

        # Get the already existing shot, created in test_base.py
        get_response = self.client.get("/shots/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/sh030",
        }
        shot_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(shot_url, data, format="json")

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Test the stored values
        self.dummy_shot.refresh_from_db()
        self.assertEqual(self.dummy_shot.root, "/sh030")
