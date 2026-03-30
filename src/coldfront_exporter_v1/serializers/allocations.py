# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import timezone

from coldfront.core.allocation.models import Allocation
from rest_framework import serializers
from rest_framework_yaml.renderers import YAMLRenderer

from .base import (
    AttributeDataField,
    NonNullModelSerializer,
    StatusField,
    UserListField,
    register_exporter,
)


class ResourceField(serializers.CharField):
    def to_representation(self, value):
        resource = value.resources.first()
        return resource.name


class AllocationSerializer(NonNullModelSerializer):
    created = serializers.DateTimeField(default_timezone=timezone.utc)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    resource = ResourceField(source="*")
    users = UserListField(source="*", user_set="allocationuser_set")
    status = StatusField(
        source="status.name",
        default_choice="renew",
        allowed_choices={
            "new": "new",
            "active": "active",
            "denied": "denied",
            "expired": "expired",
            "approved": "approved",
            "revoked": "revoked",
            "renewal requested": "renew",
            "inactive (renewed)": "renew",
        },
    )
    project = serializers.CharField(
        source="project.title",
    )
    owner = serializers.CharField(
        source="project.pi.username",
    )
    attribute_data = AttributeDataField(
        source="*", attribute_names=["slurm_specs", "slurm_user_specs"]
    )

    class Meta:
        model = Allocation
        fields = [
            "owner",
            "status",
            "resource",
            "project",
            "start_date",
            "end_date",
            "users",
            "justification",
            "created",
            "attribute_data",
        ]


def export_allocations():
    allocations = []
    for a in Allocation.objects.all():
        allocations.append(AllocationSerializer(a).data)

    return YAMLRenderer().render(allocations)


register_exporter("allocations", export_allocations)
