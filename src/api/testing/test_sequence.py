from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Sequence


class SequenceTestCase(AuthentificatedTestBase):
    def test_create_new_sequence(self):
        print("\nTesting : Create new sequence ")
        data = {
            "root": "/tars/test_pipe/seq020",
            "index": 20,
            "width": 4096,
            "height": 2160,
            "project": f"http://testserver/projects/{self.dummy_project.id}/",
        }
        response = self.client.post("/sequences/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sequence.objects.count(), 2)
        self.assertEqual(response.data["framerate"], 24.975)
        self.assertEqual(response.data["width"], 4096)

    def test_create_existing_sequence(self):
        print("\nTesting : Create existing sequence ")
        data = {
            "root": "/tars/test_pipe/seq020",
            "index": 10,
            "width": 4096,
            "height": 2160,
            "project": f"http://testserver/projects/{self.dummy_project.id}/",
        }
        response = self.client.post("/sequences/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sequence.objects.count(), 1)

    def test_get_sequence(self):
        print("\nTesting : Retrieve sequence ")
        response = self.client.get("/sequences/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sequence.objects.count(), 1)
        self.assertEqual(Sequence.objects.first().index, 10)

    def test_update_sequence(self):
        print("\nTesting : Update sequence ")
        get_response = self.client.get("/sequences/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/tars/test_pipe/seq020",
        }
        sequence_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(sequence_url, data, format="json")

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sequence.objects.count(), 1)
        self.assertEqual(Sequence.objects.first().root, "/tars/test_pipe/seq020")

    def test_remove_sequence(self):
        print("\nTesting : Delete sequence ")
        get_response = self.client.get("/sequences/")
        self.assertEqual(get_response.data["count"], 1)

        sequence_url = get_response.data["results"][0]["url"]
        delete_response = self.client.delete(sequence_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sequence.objects.count(), 0)
