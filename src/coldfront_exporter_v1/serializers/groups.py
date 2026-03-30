# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_yaml.renderers import YAMLRenderer

from .base import NonNullModelSerializer, register_exporter


class UserListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, value):
        users = []

        for u in value.user_set.all():
            users.append(u.username)

        return users


class GroupSerializer(NonNullModelSerializer):
    users = UserListField(source="*")

    class Meta:
        model = Group
        fields = [
            "users",
        ]


def export_groups():
    groups = {}
    for g in Group.objects.all():
        groups[g.name] = GroupSerializer(g).data

    return YAMLRenderer().render(groups)


register_exporter("groups", export_groups)
