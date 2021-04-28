from urllib.parse import urlparse
from django.urls import resolve
from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Shot


########################################
## Test utility
########################################


def create_new_shot(test_case):
    data = {
        "root": "/sh020",
        "index": 20,
        "width": 4096,
        "height": 2160,
        "sequence": f"http://testserver/sequences/{test_case.dummy_sequence.id}/",
    }
    return test_case.client.post("/shots/", data, format="json")


def create_existing_shot(test_case):
    data = {
        "root": "/sh020",
        "index": 10,
        "width": 4096,
        "height": 2160,
        "sequence": f"http://testserver/sequences/{test_case.dummy_sequence.id}/",
    }
    return test_case.client.post("/shots/", data, format="json")


def update_shot(test_case):
    # Get the already existing shot, created in test_base.py
    get_response = test_case.client.get(f"/shots/{test_case.dummy_shot.id}/")

    data = {
        "root": "/sh030",
    }
    shot_url = get_response.data["url"]
    return test_case.client.patch(shot_url, data, format="json")


def delete_shot(test_case):
    # Get the already existing shot, created in test_base.py
    get_response = test_case.client.get(f"/shots/{test_case.dummy_shot.id}/")

    shot_url = get_response.data["url"]
    return test_case.client.delete(shot_url)


########################################
## Running test
########################################


class ShotTestCase(AuthentificatedTestBase):
    def test_create_new_shot(self):
        print("\nTesting : Create new shot ")
        response = create_new_shot(self)
        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
            self.assertEqual(Shot.objects.count(), 2)

    def test_create_existing_shot(self):
        print("\nTesting : Create existing shot ")
        response = create_existing_shot(self)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Shot.objects.count(), 1)

    def test_retrieve_shot(self):
        # Get the already existing shot, created in test_base.py
        print("\nTesting : Retrieve shot ")
        response = self.client.get("/shots/")

        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["index"], 10)
        self.assertEqual(
            response.data["results"][0]["path"], "/tars/test_pipe/seq010/sh010"
        )
        # Test the stored values
        self.assertEqual(Shot.objects.count(), 1)
        self.assertEqual(Shot.objects.first().index, 10)

    def test_update_shot(self):
        print("\nTesting : Update shot ")
        update_response = update_shot(self)

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Test the stored values
        self.dummy_shot.refresh_from_db()
        self.assertEqual(Shot.objects.count(), 1)
        self.assertEqual(self.dummy_shot.root, "/sh030")

    def test_delete_shot(self):
        print("\nTesting : Delete shot ")
        delete_response = delete_shot(self)

        # Test the returned values
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # Test the stored values
        self.assertEqual(Shot.objects.count(), 0)
