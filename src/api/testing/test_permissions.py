from django.contrib.auth.models import Group
from rest_framework import status
from api.testing.test_base import AuthentificatedTestBase
from api.testing.test_shot import create_new_shot, update_shot, delete_shot
from api.testing.test_sequence import (
    create_new_sequence,
    update_sequence,
    delete_sequence,
)
from api.testing.test_project import create_new_project, update_project, delete_project


########################################
## Test utility
########################################


def crud_project(test_case):
    response_create = create_new_project(test_case)
    response_update = update_project(test_case)
    response_delete = delete_project(test_case)

    return response_create, response_update, response_delete


def crud_sequence(test_case):
    response_create = create_new_sequence(test_case)
    response_update = update_sequence(test_case)
    response_delete = delete_sequence(test_case)

    return response_create, response_update, response_delete


def crud_shot(test_case):
    response_create = create_new_shot(test_case)
    response_update = update_shot(test_case)
    response_delete = delete_shot(test_case)

    return response_create, response_update, response_delete


########################################
## Running test
########################################


class PermissionsTestCase(AuthentificatedTestBase):
    def test_project_ownership_authorisation(self):
        print("\nTesting : CRUD on projects with different ownership relation")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # CRUD unauthorized project
        response_create, response_update, response_delete = crud_project(self)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)

        # Add dummy_project to dummy_user's projects
        self.dummy_user.projects.set(
            [
                self.dummy_project,
            ]
        )
        self.dummy_user.save()

        # CRUD authorized project
        response_create, response_update, response_delete = crud_project(self)
        # Here we expect a bad request because the project should already exist
        self.assertEqual(response_create.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_project_permission_elevation(self):
        print("\nTesting : CRUD on projects with different elevated permissions")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Attach the user to the developper_group so he gets all right
        developper_group = Group.objects.get(name="developper")
        self.dummy_user.groups.add(developper_group)
        self.dummy_user.save()

        # CRUD authorized project
        response_create, response_update, response_delete = crud_project(self)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_sequence_ownership_authorisation(self):
        print("\nTesting : CRUD on sequences with different ownership relation")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # CRUD unauthorized sequence
        response_create, response_update, response_delete = crud_sequence(self)
        self.assertEqual(response_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)

        # Add dummy_project to dummy_user's projects
        self.dummy_user.projects.set(
            [
                self.dummy_project,
            ]
        )
        self.dummy_user.save()

        # CRUD authorized sequence
        response_create, response_update, response_delete = crud_sequence(self)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_sequence_permission_elevation(self):
        print("\nTesting : CRUD on sequences with different elevated permissions")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Attach the user to the developper_group so he gets all right
        developper_group = Group.objects.get(name="developper")
        self.dummy_user.groups.add(developper_group)
        self.dummy_user.save()

        # CRUD authorized sequence
        response_create, response_update, response_delete = crud_sequence(self)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_shot_ownership_authorisation(self):
        print("\nTesting : CRUD on shots with different ownership relation")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # CRUD unauthorized shot
        response_create, response_update, response_delete = crud_shot(self)
        self.assertEqual(response_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)

        # Add dummy_project to dummy_user's projects
        self.dummy_user.projects.set(
            [
                self.dummy_project,
            ]
        )
        self.dummy_user.save()

        # CRUD authorized shot
        response_create, response_update, response_delete = crud_shot(self)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_shot_permission_elevation(self):
        print("\nTesting : CRUD on shots with different elevated permissions")
        # Login as dummy_user
        self.client.force_authenticate(self.dummy_user)
        # Attach the user to the developper_group so he gets all right
        developper_group = Group.objects.get(name="developper")
        self.dummy_user.groups.add(developper_group)
        self.dummy_user.save()

        # CRUD authorized shot
        response_create, response_update, response_delete = crud_shot(self)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
