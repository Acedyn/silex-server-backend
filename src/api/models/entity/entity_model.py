from django.db.models import (
    Model,
    CharField,
    FloatField,
    PositiveIntegerField,
    DateTimeField,
    ForeignKey,
    SET_NULL,
)
from django.utils import timezone
from api.validators import path_validator, state_validator

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
## SQL tables
########################################


class Entity(Model):
    # Fields
    deleted_at = DateTimeField(null=True)
    updated_at = DateTimeField(default=timezone.now)
    created_at = DateTimeField(default=timezone.now)
    root = CharField(validators=[path_validator], max_length=250, null=True)
    state = CharField(validators=[state_validator], max_length=10)
    framerate = FloatField(default=25.0)
    width = PositiveIntegerField(default=1920)
    height = PositiveIntegerField(default=1080)

    # Abstract fields
    project: ForeignKey
    deleted_by: ForeignKey
    updated_by: ForeignKey
    created_by: ForeignKey

    # Dynamicaly created field
    @classmethod
    def create_dynamic_fields(cls):
        class_name = cls.__name__.lower()

        deleted_by = ForeignKey(
            "User", on_delete=SET_NULL, null=True, related_name=f"deleted_{class_name}s"
        )
        deleted_by.contribute_to_class(cls, "target")
        updated_by = ForeignKey(
            "User", on_delete=SET_NULL, null=True, related_name=f"updated_{class_name}s"
        )
        updated_by.contribute_to_class(cls, "target")
        created_by = ForeignKey(
            "User", on_delete=SET_NULL, null=True, related_name=f"created_{class_name}s"
        )
        created_by.contribute_to_class(cls, "target")

    class Meta:
        abstract = True
