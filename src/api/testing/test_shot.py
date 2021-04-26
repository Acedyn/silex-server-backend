from urllib.parse import urlparse
from django.urls import resolve
from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Shot


class ShotTestCase(AuthentificatedTestBase):
    def test_create_new_shot(self):
        print("\nTesting : Create new shot ")
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
        self.assertEqual(Shot.objects.count(), 2)
        self.assertEqual(response.data["framerate"], 24.975)
        self.assertEqual(response.data["width"], 4096)
        shot_path = urlparse(response.data["url"]).path
        # Test the stored values
        try:
            shot_match = resolve(shot_path)
            shot_queryset = Shot.objects.all()
            self.shot = shot_queryset.get(id=shot_match.kwargs["pk"])
        except Exception as ex:
            self.fail(
                f"ERROR: {type(ex)} : \
                Could not get shot instance from shot url {shot_path}"
            )
        finally:
            self.assertEqual(self.shot.framerate, 24.975)
            self.assertEqual(self.shot.width, 4096)

    def test_create_existing_shot(self):
        print("\nTesting : Create existing shot ")
        data = {
            "root": "/sh020",
            "index": 10,
            "width": 4096,
            "height": 2160,
            "sequence": f"http://testserver/sequences/{self.dummy_sequence.id}/",
        }
        response = self.client.post("/shots/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Shot.objects.count(), 1)

    def test_retrieve_shot(self):
        # Get the already existing shot, created in test_base.py
        print("\nTesting : Retrieve shot ")
        response = self.client.get("/shots/")

        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["index"], 20)
        self.assertEqual(
            response.data["results"][0]["path"], "/tars/test_pipe/seq010/sh020"
        )
        # Test the stored values
        self.assertEqual(Shot.objects.count(), 1)
        self.assertEqual(Shot.objects.first().index, 20)

    def test_update_shot(self):
        print("\nTesting : Update shot ")
        # Get the already existing shot, created in test_base.py
        get_response = self.client.get("/shots/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/sh30",
        }
        shot_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(shot_url, data, format="json")

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Shot.objects.count(), 1)
        self.assertEqual(Shot.objects.first().root, "/sh30")
        # Test the stored values
        self.dummy_shot.refresh_from_db()
        self.assertEqual(self.dummy_shot.root, "/sh30")

    def test_delete_shot(self):
        print("\nTesting : Delete shot ")
        # Get the already existing shot, created in test_base.py
        get_response = self.client.get("/shots/")
        self.assertEqual(get_response.data["count"], 1)

        shot_url = get_response.data["results"][0]["url"]
        delete_response = self.client.delete(shot_url)

        # Test the returned values
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # Test the stored values
        self.assertEqual(Shot.objects.count(), 0)
