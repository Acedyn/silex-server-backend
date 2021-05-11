import random
from django.db.models import (
    Model,
    CharField,
    BooleanField,
    FloatField,
    SlugField,
    PositiveIntegerField,
    DateTimeField,
    EmailField,
    ManyToManyField,
    ForeignKey,
    CASCADE,
    SET_NULL,
    Q,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from api.validators import path_validator, color_validator, state_validator

########################################
## Utility
########################################


# Used as default value for color field in the Project model
def random_hexa_color() -> str:
    random_color = lambda: random.randint(0, 255)
    return "#%02X%02X%02X" % (random_color(), random_color(), random_color())


########################################
## Permissions
########################################
project_ownership_permissions = [
    (
        "add_any_entity",
        "Can add entity that belong to a project the user does not own",
    ),
    (
        "change_any_entity",
        "Can change entity that belong to a project the user does not own",
    ),
    (
        "delete_any_entity",
        "Can delete entity that belong to a project the user does not own",
    ),
]


########################################
## Tables for the silex_server_backend database
########################################


class Base(Model):
    deleted_at = DateTimeField(null=True)
    updated_at = DateTimeField(default=timezone.now)
    created_at = DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Metadata(Model):
    root = CharField(validators=[path_validator], max_length=250, null=True)
    state = CharField(validators=[state_validator], max_length=10)
    framerate = FloatField(default=25.0)
    width = PositiveIntegerField(default=1920)
    height = PositiveIntegerField(default=1080)

    class Meta:
        abstract = True


class Project(Base, Metadata):
    name = SlugField(default="untitled", unique=True)
    label = CharField(default="untitled", max_length=50)
    color = CharField(
        validators=[color_validator], max_length=7, default=random_hexa_color
    )
    # We need to set these individualy because of the related_name argument
    deleted_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="deleted_projects"
    )
    updated_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="updated_projects"
    )
    created_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="created_projects"
    )

    class Meta:
        ordering = ["-id"]
        unique_together = (("root"),)


class Sequence(Base, Metadata):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="sequences")
    # We need to set these individualy because of the related_name argument
    deleted_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="deleted_sequences"
    )
    updated_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="updated_sequences"
    )
    created_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="created_sequences"
    )

    class Meta:
        unique_together = (("index", "project"), ("project", "root"))
        ordering = ["-id"]
        permissions = project_ownership_permissions


class Shot(Base, Metadata):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="shots")
    sequence = ForeignKey(Sequence, on_delete=CASCADE, related_name="shots")
    # We need to set these individualy because of the related_name argument
    deleted_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="deleted_shots"
    )
    updated_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="updated_shots"
    )
    created_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="created_shots"
    )

    class Meta:
        unique_together = (
            ("index", "project", "sequence"),
            ("project", "sequence", "root"),
        )
        ordering = ["-id"]
        permissions = project_ownership_permissions

    # Override the save() method to auto fill the project field with the given sequence
    def save(self, *args, **kwargs):
        self.project = self.sequence.project
        super().save(*args, **kwargs)


class Frame(Base, Metadata):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="frames")
    sequence = ForeignKey(Sequence, on_delete=CASCADE, related_name="frames")
    shot = ForeignKey(Shot, on_delete=CASCADE, related_name="frames")
    valid = BooleanField(default=False)
    # We need to set these individualy because of the related_name argument
    deleted_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="deleted_frames"
    )
    updated_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="updated_frames"
    )
    created_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="created_frames"
    )

    class Meta:
        unique_together = (
            ("index", "project", "sequence", "shot"),
            ("project", "sequence", "shot", "root"),
        )
        ordering = ["-id"]
        permissions = project_ownership_permissions

    # Override the save() method to auto fill the project and sequence fields with the given shot
    def save(self, *args, **kwargs):
        self.sequence = self.shot.sequence
        self.project = self.shot.project
        super().save(*args, **kwargs)


class Asset(Base, Metadata):
    project = ForeignKey(Project, on_delete=CASCADE, related_name="assets")
    name = SlugField(default="untitled", unique=True)
    label = CharField(default="untitled", max_length=250)
    # We need to set these individualy because of the related_name argument
    deleted_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="deleted_assets"
    )
    updated_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="updated_assets"
    )
    created_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="created_assets"
    )

    class Meta:
        unique_together = (("name", "project"), ("project", "root"))
        ordering = ["-id"]
        permissions = project_ownership_permissions


class Task(Base, Metadata):
    project = ForeignKey(Project, on_delete=CASCADE, related_name="tasks")
    name = SlugField(default="untitled")
    label = CharField(default="untitled", max_length=250)
    # We need to set these individualy because of the related_name argument
    deleted_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="deleted_tasks"
    )
    updated_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="updated_tasks"
    )
    created_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name="created_tasks"
    )

    limit = (
        Q(app_label="api", model="Sequence")
        | Q(app_label="api", model="Shot")
        | Q(app_label="api", model="Asset")
    )

    entity_type = ForeignKey(
        ContentType, on_delete=CASCADE, limit_choices_to=limit, null=True
    )
    entity_id = PositiveIntegerField(null=True)
    entity_object = GenericForeignKey("entity_type", "entity_id")

    class Meta:
        ordering = ["-id"]


class User(AbstractUser):
    projects = ManyToManyField(Project)
    email = EmailField(unique=True)
