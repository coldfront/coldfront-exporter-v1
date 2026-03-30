# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import os

from django.core.management.base import BaseCommand, CommandError

from coldfront_exporter_v1.serializers import EXPORTER_REGISTRY


class Command(BaseCommand):
    help = "Export database to yaml files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            action="store",
            help="Output directory",
            required=True,
        )

    def handle(self, *args, **options):
        output_dir = options["output"]
        if not output_dir:
            raise CommandError("output option cannot be empty.")

        if not os.path.isdir(output_dir):
            raise CommandError("output path must be a directory.")

        for fname, exporter_func in EXPORTER_REGISTRY.items():
            dst_file = f"{output_dir}/{fname}.yml"
            if os.path.isfile(dst_file):
                self.stdout.write(
                    self.style.WARNING(
                        f"Warning: Destination file exists {fname}.yml. File will not be overwritten."
                    )
                )
                continue

            data = exporter_func()
            with open(dst_file, "wb") as fh:
                fh.write(data)
