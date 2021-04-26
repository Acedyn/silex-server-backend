from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Shot


class ShotTestCase(AuthentificatedTestBase):
    def test_create_new_shot(self):
        print("\nTesting : Create new shot ")
        data = {
            "root": "/tars/test_pipe/seq020/sh030",
            "index": 30,
            "width": 4096,
            "height": 2160,
            "project": f"http://testserver/projects/{self.dummy_project.id}/",
            "sequence": f"http://testserver/sequences/{self.dummy_sequence.id}/",
        }
        response = self.client.post("/shots/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shot.objects.count(), 2)
        self.assertEqual(response.data["framerate"], 24.975)
        self.assertEqual(response.data["width"], 4096)

    def test_create_existing_shot(self):
        print("\nTesting : Create existing shot ")
        data = {
            "root": "/tars/test_pipe/seq010/sh020",
            "index": 10,
            "width": 4096,
            "height": 2160,
            "project": f"http://testserver/projects/{self.dummy_project.id}/",
            "sequence": f"http://testserver/sequences/{self.dummy_sequence.id}/",
        }
        response = self.client.post("/shots/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Shot.objects.count(), 1)

    def test_get_shot(self):
        print("\nTesting : Retrieve shot ")
        response = self.client.get("/shots/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Shot.objects.count(), 1)
        self.assertEqual(Shot.objects.first().index, 20)

    def test_update_shot(self):
        print("\nTesting : Update shot ")
        get_response = self.client.get("/shots/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/tars/test_pipe/seq020/sh50",
        }
        shot_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(shot_url, data, format="json")

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Shot.objects.count(), 1)
        self.assertEqual(Shot.objects.first().root, "/tars/test_pipe/seq020/sh50")

    def test_remove_shot(self):
        print("\nTesting : Delete shot ")
        get_response = self.client.get("/shots/")
        self.assertEqual(get_response.data["count"], 1)

        shot_url = get_response.data["results"][0]["url"]
        delete_response = self.client.delete(shot_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Shot.objects.count(), 0)
