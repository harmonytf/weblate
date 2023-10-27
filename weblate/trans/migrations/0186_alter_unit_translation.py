# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Generated by Django 4.2.3 on 2023-09-05 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trans", "0185_alter_component_allow_translation_propagation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unit",
            name="translation",
            field=models.ForeignKey(
                db_index=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="trans.translation",
            ),
        ),
    ]
