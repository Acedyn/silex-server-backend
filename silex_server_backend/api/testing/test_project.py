from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Project

class ProjectTestCase(AuthentificatedTestBase):
    def test_create_new_project(self):
        print("\nTesting : Create new project")
        data = {'root': '/anna/hello_world', 'framerate': 25, 'width': 4096, 'height': 2160, 'label': 'Hello World!'}
        response = self.client.post("/projects/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)


    def test_get_project(self):
        print("\nTesting : Get project")
        response = self.client.get("/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'test-pipe')

