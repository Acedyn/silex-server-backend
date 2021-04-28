from urllib.parse import urlparse
from django.urls import resolve
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from api.models import Metadata


def get_instance_from_url(
    url: str, instance_class: Metadata, error_name: str = "ERROR"
) -> Metadata:
    try:
        instance_path = urlparse(url).path
        instance_match = resolve(instance_path)
        instance_queryset = instance_class.objects.all()
        instance = instance_queryset.get(id=instance_match.kwargs["pk"])
        return instance
    except Exception as ex:
        # If the parent could not be resolved, raise an exception
        raise ValidationError(
            {f"{error_name}": "Could not find inheritance tree for this parent."}
        ) from ex


# Add missing fiel
def request_inherit_fields(data, request, parents_chain, parent_model_class):
    # Check is the parent is given
    if parents_chain[0] not in data:
        return data

    parent = None

    # Get the project from the url
    parent = get_instance_from_url(
        data[parents_chain[0]], parent_model_class, parents_chain[0]
    )

    # Override the fields that where not set in the input request
    if "framerate" not in data:
        data["framerate"] = parent.framerate
    if "width" not in data:
        data["width"] = parent.width
    if "height" not in data:
        data["height"] = parent.height

    # Add all the parenting chain
    sub_parents = (parent for parent in parents_chain if parent != parents_chain[0])
    for sub_parent in sub_parents:
        # Build the url that lead to the sub_parent
        sub_parent_url = (
            str(reverse(viewname=f"{sub_parent}-list", request=request))
            + f"{str(getattr(parent, sub_parent).id)}/"
        )
        data[sub_parent] = sub_parent_url

    return data
