# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import timezone

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_yaml.renderers import YAMLRenderer

from .base import NonNullModelSerializer, register_exporter


class UserSerializer(NonNullModelSerializer):
    date_joined = serializers.DateTimeField(default_timezone=timezone.utc)
    password_hash = serializers.CharField(source="password")

    class Meta:
        model = User
        fields = [
            "password_hash",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        ]


def export_users():
    users = {}
    for u in User.objects.all():
        users[u.username] = UserSerializer(u).data

    return YAMLRenderer().render(users)


register_exporter("users", export_users)
