# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from collections import OrderedDict

from django.utils.text import slugify
from rest_framework import serializers


class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super(NonNullModelSerializer, self).to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )


class StatusField(serializers.CharField):
    def __init__(self, *args, default_choice=None, allowed_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_choices = allowed_choices
        self.default_choice = default_choice

    def to_representation(self, value):
        choice = value.lower()
        if choice not in self.allowed_choices:
            return self.default_choice

        if isinstance(self.allowed_choices, dict):
            choice = self.allowed_choices[choice]

        return choice


class SlugField(serializers.SlugField):
    def to_representation(self, value):
        return slugify(value)


class UserListField(serializers.ListField):
    child = serializers.CharField()

    def __init__(self, *args, user_set=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_set = user_set

    def to_representation(self, value):
        users = []

        user_set = getattr(value, self.user_set, None)
        if user_set:
            for u in user_set.filter(status__name="Active"):
                users.append(u.user.username)

        return users


class AttributeDataField(serializers.CharField):
    def __init__(self, *args, attribute_names=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute_names = attribute_names

    def to_representation(self, value):
        data = {}
        for att in self.attribute_names:
            att_val = value.get_attribute(att)
            if att_val:
                data[att] = att_val
        return data if data else None


EXPORTER_REGISTRY = dict()


def register_exporter(name: str, exporter):
    EXPORTER_REGISTRY[name] = exporter
