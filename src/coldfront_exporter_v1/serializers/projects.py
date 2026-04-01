# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import timezone

from coldfront.core.project.models import Project
from rest_framework import serializers
from rest_framework_yaml.renderers import YAMLRenderer

from .base import (
    NonNullModelSerializer,
    SlugField,
    StatusField,
    UserListField,
    register_exporter,
)


class CustomFieldDataField(serializers.CharField):
    def to_representation(self, value):
        data = {}
        if value.field_of_science:
            data["nfs_fos"] = str(value.field_of_science.fos_nsf_id)
        else:
            data["nfs_fos"] = None

        return data


class ProjectSerializer(NonNullModelSerializer):
    created = serializers.DateTimeField(default_timezone=timezone.utc)
    custom_field_data = CustomFieldDataField(source="*")
    users = UserListField(source="*", user_set="projectuser_set")
    slug = SlugField(source="title")
    name = serializers.CharField(
        source="title",
    )
    status = StatusField(
        source="status.name",
        default_choice="active",
        allowed_choices=["active", "archived"],
    )
    owner = serializers.CharField(
        source="pi.username",
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "slug",
            "description",
            "owner",
            "custom_field_data",
            "status",
            "users",
            "created",
        ]


def export_projects():
    projects = []
    for p in Project.objects.filter(status__name="Active"):
        projects.append(ProjectSerializer(p).data)

    return YAMLRenderer().render(projects)


register_exporter("projects", export_projects)
