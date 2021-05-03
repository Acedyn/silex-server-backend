from urllib.parse import urlparse
from django.urls import resolve
from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.models import Project


########################################
## Test utility
########################################


def create_new_project(test_case):
    data = {
        "root": "/anna/hello_world",
        "width": 4096,
        "height": 2160,
        "label": "Hello World!",
    }
    return test_case.client.post("/projects/", data, format="json")


def create_existing_project(test_case):
    data = {
        "root": "/tars/hello_world",
        "framerate": 25,
        "width": 4096,
        "height": 2160,
        "label": "Test Pipe",
    }
    return test_case.client.post("/projects/", data, format="json")


def update_project(test_case):
    # Get the already existing project, created in test_base.py
    get_response = test_case.client.get(f"/projects/{test_case.dummy_project.id}/")

    data = {
        "root": "/tars/hello_world",
    }
    project_url = get_response.data["url"]
    return test_case.client.patch(project_url, data, format="json")


def delete_project(test_case):
    # Get the already existing project, created in test_base.py
    get_response = test_case.client.get(f"/projects/{test_case.dummy_project.id}/")

    project_url = get_response.data["url"]
    return test_case.client.delete(project_url)


########################################
## Running test
########################################


class ProjectTestCase(AuthentificatedTestBase):
    def test_create_new_project(self):
        print("\nTesting : Create new project ")
        response = create_new_project(self)
        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["framerate"], 25.0)
        self.assertEqual(response.data["width"], 4096)
        project_path = urlparse(response.data["url"]).path
        # Test the stored values
        try:
            project_match = resolve(project_path)
            project_queryset = Project.objects.all()
            self.project = project_queryset.get(id=project_match.kwargs["pk"])
        except Exception as ex:
            self.fail(
                f"ERROR: {type(ex)} : \
                Could not get project instance from sequence url {project_path}"
            )
        finally:
            self.assertEqual(self.project.framerate, 25.0)
            self.assertEqual(self.project.width, 4096)
            self.assertEqual(Project.objects.count(), 2)

    def test_create_existing_project(self):
        print("\nTesting : Create existing project ")
        response = create_existing_project(self)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Project.objects.count(), 1)

    def test_retrieve_project(self):
        print("\nTesting : Retrieve project ")
        # Get the already existing project, created in test_base.py
        response = self.client.get("/projects/")

        # Test the returned values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], "test-pipe")
        self.assertEqual(response.data["results"][0]["path"], "/tars/test_pipe")
        # Test the stored values
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().name, "test-pipe")

    def test_update_project(self):
        print("\nTesting : Update project ")
        update_response = update_project(self)

        # Test the returned values
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().root, "/tars/hello_world")
        # Test the stored values
        self.dummy_project.refresh_from_db()
        self.assertEqual(self.dummy_project.root, "/tars/hello_world")

    def test_delete_project(self):
        print("\nTesting : Delete project ")
        delete_response = delete_project(self)

        # Test the returned values
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # Test the stored values
        self.assertEqual(Project.objects.count(), 0)
