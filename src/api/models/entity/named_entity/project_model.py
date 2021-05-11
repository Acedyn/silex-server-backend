import random
from django.db.models import CharField
from api.models.entity.named_entity.named_entity_model import NamedEntity
from api.validators import color_validator


########################################
## Utility
########################################


# Used as default value for color field in the Project model
def random_hexa_color() -> str:
    random_color = lambda: random.randint(0, 255)
    return "#%02X%02X%02X" % (random_color(), random_color(), random_color())


########################################
## Tables for the silex_server_backend database
########################################


class ProjectTest(NamedEntity):
    color = CharField(
        validators=[color_validator], max_length=7, default=random_hexa_color
    )

    class Meta:
        ordering = ["-id"]
        unique_together = (("root"),)
