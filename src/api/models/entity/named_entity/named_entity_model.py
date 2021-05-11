from django.db.models import SlugField, CharField
import api.models.entity.entity_model import Entity


########################################
## Tables for the silex_server_backend database
########################################


class NamedEntity(Entity):
    name = SlugField(default="untitled", unique=True)
    label = CharField(default="untitled", max_length=50)

    class Meta:
        abstract = True
