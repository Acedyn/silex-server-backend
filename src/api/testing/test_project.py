from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Project


class ProjectTestCase(AuthentificatedTestBase):
    def test_create_new_project(self):
        print("\nTesting : Create new project ")
        data = {
            "root": "/anna/hello_world",
            "framerate": 25,
            "width": 4096,
            "height": 2160,
            "label": "Hello World!",
            "name": "hello-world",
        }
        response = self.client.post("/projects/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_create_existing_project(self):
        print("\nTesting : Create existing project ")
        data = {
            "root": "/tars/hello_world",
            "framerate": 25,
            "width": 4096,
            "height": 2160,
            "label": "TEST PIPE",
            "name": "test-pipe",
        }
        response = self.client.post("/projects/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Project.objects.count(), 1)

    def test_get_project(self):
        print("\nTesting : Retrieve project ")
        response = self.client.get("/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().name, "test-pipe")

    def test_update_project(self):
        print("\nTesting : Update project ")
        get_response = self.client.get("/projects/")
        self.assertEqual(get_response.data["count"], 1)

        data = {
            "root": "/tars/hello_world",
        }
        project_url = get_response.data["results"][0]["url"]
        update_response = self.client.patch(project_url, data, format="json")

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().root, "/tars/hello_world")

    def test_remove_project(self):
        print("\nTesting : Delete project ")
        get_response = self.client.get("/projects/")
        self.assertEqual(get_response.data["count"], 1)

        project_url = get_response.data["results"][0]["url"]
        delete_response = self.client.delete(project_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)
