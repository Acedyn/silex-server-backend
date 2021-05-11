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
    root = CharField(validators=[path_validator], max_length=250, null=True)
    state = CharField(validators=[state_validator], max_length=10)
    framerate = FloatField(default=25.0)
    width = PositiveIntegerField(default=1920)
    height = PositiveIntegerField(default=1080)

    deleted_at = DateTimeField(null=True)
    updated_at = DateTimeField(default=timezone.now)
    created_at = DateTimeField(default=timezone.now)
    deleted_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name=f"deleted_%(class)s"
    )
    updated_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name=f"updated_%(class)s"
    )
    created_by = ForeignKey(
        "User", on_delete=SET_NULL, null=True, related_name=f"created_%(class)s"
    )

    class Meta:
        abstract = True
