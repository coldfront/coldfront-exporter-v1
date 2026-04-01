# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import timezone

from coldfront.core.resource.models import Resource
from rest_framework import serializers
from rest_framework_yaml.renderers import YAMLRenderer

from .base import (
    AttributeDataField,
    NonNullModelSerializer,
    SlugField,
    register_exporter,
)


class ResourceSerializer(NonNullModelSerializer):
    created = serializers.DateTimeField(default_timezone=timezone.utc)
    slug = SlugField(source="name")
    attribute_data = AttributeDataField(
        source="*", attribute_names=["slurm_cluster", "slurm_specs"]
    )
    resource_type = serializers.CharField(
        source="resource_type.name",
    )
    parent = serializers.CharField(
        source="parent_resource.name",
        allow_null=True,
    )

    class Meta:
        model = Resource
        fields = [
            "name",
            "slug",
            "parent",
            "attribute_data",
            "description",
            "is_allocatable",
            "resource_type",
            "created",
        ]


def export_child_resources(resource):
    resources = [ResourceSerializer(resource).data]
    for r in Resource.objects.filter(parent_resource=resource):
        resources.extend(export_child_resources(r))

    return resources


def export_resources():
    resources = []
    for r in Resource.objects.filter(parent_resource__isnull=True):
        resources.extend(export_child_resources(r))

    return YAMLRenderer().render(resources)


register_exporter("resources", export_resources)
