from urllib.parse import urlparse
from django.urls import resolve
from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Sequence


########################################
## Test utility
########################################


def create_new_sequence(test_case):
    data = {
        "root": "/seq020",
        "index": 20,
        "width": 4096,
        "height": 2160,
        "project": f"http://testserver/projects/{test_case.dummy_project.id}/",
    }
    return test_case.client.post("/sequences/", data, format="json")


def create_existing_sequence(test_case):
    data = {
        "root": "/seq020",
        "index": 10,
        "width": 4096,
        "height": 2160,
        "project": f"http://testserver/projects/{test_case.dummy_project.id}/",
    }
    return test_case.client.post("/sequences/", data, format="json")


def update_sequence(test_case):
    # Get the already existing sequence, created in test_base.py
    get_response = test_case.client.get(f"/sequences/{test_case.dummy_sequence.id}/")

    data = {
        "root": "/seq030",
    }
    sequence_url = get_response.data["url"]
    return test_case.client.patch(sequence_url, data, format="json")


def delete_sequence(test_case):
    # Get the already existing sequence, created in test_base.py
    get_response = test_case.client.get(f"/sequences/{test_case.dummy_sequence.id}/")

    sequence_url = get_response.data["url"]
    return test_case.client.delete(sequence_url)


########################################
## Running test
########################################


class SequenceTestCase(AuthentificatedTestBase):
    def test_create_new_sequence(self):
        print("\nTesting : Create new sequence ")
        response = create_new_sequence(self)
        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["framerate"], 24.975)
        self.assertEqual(response.data["width"], 4096)
        sequence_path = urlparse(response.data["url"]).path
        # Test the stored values
        try:
            sequence_match = resolve(sequence_path)
            sequence_queryset = Sequence.objects.all()
            self.sequence = sequence_queryset.get(id=sequence_match.kwargs["pk"])
        except Exception as ex:
            self.fail(
                f"ERROR: {type(ex)} : \
                Could not get sequence instance from sequence url {sequence_path}"
            )
        finally:
            self.assertEqual(self.sequence.framerate, 24.975)
            self.assertEqual(self.sequence.width, 4096)
            self.assertEqual(Sequence.objects.count(), 2)

    def test_create_existing_sequence(self):
        print("\nTesting : Create existing sequence ")
        response = create_existing_sequence(self)

        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test the stored values
        self.assertEqual(Sequence.objects.count(), 1)

    def test_retrieve_sequence(self):
        print("\nTesting : Retrieve sequence ")
        # Get the already existing sequence, created in test_base.py
        response = self.client.get("/sequences/")

        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["index"], 10)
        self.assertEqual(response.data["results"][0]["path"], "/tars/test_pipe/seq010")
        # Test the stored values
        self.assertEqual(Sequence.objects.count(), 1)
        self.assertEqual(Sequence.objects.first().index, 10)

    def test_update_sequence(self):
        print("\nTesting : Update sequence ")
        update_response = update_sequence(self)

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Test the stored values
        self.dummy_sequence.refresh_from_db()
        self.assertEqual(Sequence.objects.count(), 1)
        self.assertEqual(self.dummy_sequence.root, "/seq030")

    def test_delete_sequence(self):
        print("\nTesting : Delete sequence ")
        delete_response = delete_sequence(self)

        # Test the returned values
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # Test the stored values
        self.assertEqual(Sequence.objects.count(), 0)
