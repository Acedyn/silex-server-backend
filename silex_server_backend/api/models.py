from django.db.models import Model
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import SlugField
from django.db.models import PositiveIntegerField
from django.db.models import DateTimeField
from django.db.models import CASCADE
from django.utils.text import slugify
from datetime import datetime

########################################
## Tables for the silex_server_backend database
########################################

class Base(Model):
    deleted_at = DateTimeField(null=True)
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)
    framerate = FloatField(default=25.0)
    width = PositiveIntegerField(default=1920)
    height = PositiveIntegerField(default=1080)

    class Meta:
        abstract = True

class Project(Base):
    name = SlugField(default="untitled")
    label = CharField(default="untitled", max_length=250)
    root = CharField(max_length=250)

    def save(self, *args, **kwargs):
        self.name = slugify(self.name).replace("-", "_").replace(" ", "_")
        return super().save(*args, **kwargs)

class Sequence(Base):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="sequences")

    class Meta:
        unique_together = (("index", "project"),)

class Shot(Base):
    index = PositiveIntegerField()
    project = ForeignKey(Project, on_delete=CASCADE, related_name="shots")
    sequence = ForeignKey(Sequence, on_delete=CASCADE, related_name="shots")

    class Meta:
        unique_together = (("index", "project", "sequence"),)

class Frame(Base):
    index = PositiveIntegerField()
    shot = ForeignKey(Shot, on_delete=CASCADE, related_name="frames")
    project = ForeignKey(Project, on_delete=CASCADE, related_name="frames")
    sequence = ForeignKey(Sequence, on_delete=CASCADE, related_name="frames")
    valid = BooleanField(default=False)

    class Meta:
        unique_together = (("index", "project", "sequence", "shot"),)

class Asset(Base):
    project = ForeignKey(Project, on_delete=CASCADE, related_name="assets")
    name = SlugField(default="untitled")
    label = CharField(default="untitled", max_length=250)

    def save(self, *args, **kwargs):
        self.name = slugify(self.label).replace("-", "_").replace(" ", "_")
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = (("name", "project"),)

class Task(Base):
    project = ForeignKey(Project, on_delete=CASCADE, related_name="tasks")
    code = SlugField(default="untitled")
    name = CharField(default="untitled", max_length=250)
