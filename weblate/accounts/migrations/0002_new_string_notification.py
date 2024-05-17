# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Generated by Django 4.2.5 on 2023-10-12 08:25

from django.db import migrations


def migrate_subscription(apps, schema_editor) -> None:
    Subscription = apps.get_model("accounts", "Subscription")
    # Change instant to daily, because this now has string granularity
    Subscription.objects.filter(
        notification="NewStringNotificaton", frequency=1
    ).update(frequency=2)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_squashed_weblate_5"),
        ("trans", "0006_alter_change_action"),
    ]

    operations = [
        migrations.RunPython(
            migrate_subscription, migrations.RunPython.noop, elidable=True
        ),
    ]
