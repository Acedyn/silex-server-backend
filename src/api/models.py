import random
from django.db.models import (
    Model,
    CharField,
    BooleanField,
    FloatField,
    SlugField,
    PositiveIntegerField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    Q,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.text import slugify
from api.validators import path_validator, color_validator

########################################
## Utility
########################################


def random_hexa_color() -> str:
    random_color = lambda: random.randint(0, 255)
    return "#%02X%02X%02X" % (random_color(), random_color(), random_color())


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
    root = CharField(
        validators=[path_validator], max_length=250, null=True, unique=True
    )
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

    class Meta:
        ordering = ["-id"]


class Sequence(Base, Metadata):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="sequences")

    class Meta:
        unique_together = (("index", "project"),)
        ordering = ["-id"]


class Shot(Base):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="shots")
    sequence = ForeignKey(Sequence, on_delete=CASCADE, related_name="shots")

    class Meta:
        unique_together = (("index", "project", "sequence"),)
        ordering = ["-id"]


class Frame(Base):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="frames")
    sequence = ForeignKey(Sequence, on_delete=CASCADE, related_name="frames")
    shot = ForeignKey(Shot, on_delete=CASCADE, related_name="frames")
    valid = BooleanField(default=False)

    class Meta:
        unique_together = (("index", "project", "sequence", "shot"),)
        ordering = ["-id"]


class Asset(Base):
    project = ForeignKey(Project, on_delete=CASCADE, related_name="assets")
    name = SlugField(default="untitled", unique=True)
    label = CharField(default="untitled", max_length=250)

    def save(self, *args, **kwargs):
        self.name = slugify(self.label).replace("-", "_").replace(" ", "_")
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = (("name", "project"),)
        ordering = ["-id"]


class Task(Base):
    project = ForeignKey(Project, on_delete=CASCADE, related_name="tasks")
    name = SlugField(default="untitled")
    label = CharField(default="untitled", max_length=250)

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
