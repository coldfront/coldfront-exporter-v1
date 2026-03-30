# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import timezone

from coldfront.core.resource.models import ResourceType
from rest_framework import serializers
from rest_framework_yaml.renderers import YAMLRenderer

from .base import (
    NonNullModelSerializer,
    SlugField,
    register_exporter,
)


class ResourceTypeSerializer(NonNullModelSerializer):
    created = serializers.DateTimeField(default_timezone=timezone.utc)
    slug = SlugField(source="name")

    class Meta:
        model = ResourceType
        fields = [
            "name",
            "slug",
            "description",
            "created",
        ]


def export_resource_types():
    resource_types = []
    for r in ResourceType.objects.all():
        resource_types.append(ResourceTypeSerializer(r).data)

    return YAMLRenderer().render(resource_types)


register_exporter("resource_types", export_resource_types)
