# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Generated by Django 4.1.3 on 2023-01-05 09:30

from datetime import timedelta

from django.db import migrations
from django.utils import timezone

# Historical ID of changes metric
METRIC_CHANGES = 18


def migrate_metrics(apps, schema_editor):
    Metric = apps.get_model("metrics", "Metric")
    MetricFuture = apps.get_model("metrics", "MetricFuture")
    create = []
    current = None
    cutoff = timezone.now().date() - timedelta(days=65)
    current_data = {}
    db_alias = schema_editor.connection.alias
    metrics = Metric.objects.using(db_alias).filter(
        date__gte=timezone.now().date() - timedelta(days=800)
    )
    if not metrics.exists():
        return
    print("Converting metric entries, this might take long", flush=True)  # noqa: T201
    for pos, metric in enumerate(
        metrics.order_by("date", "scope", "relation", "secondary").iterator()
    ):
        # This was bug in the migration
        if metric.kind == 0:
            continue

        # Indicate progress
        if pos % 10000 == 0:
            print("*", end="", flush=True)  # noqa: T201

        # Store previous object on change
        if current is not None and (
            current.date != metric.date
            or current.scope != metric.scope
            or current.relation != metric.relation
            or current.secondary != metric.secondary
        ):
            current.changes = current_data.pop(METRIC_CHANGES, 0)
            if current.date > cutoff:
                current.data = [
                    current_data.get(i, 0) for i in range(28) if i != METRIC_CHANGES
                ]
            create.append(current)
            current = None

            # Use bulk create for more effective inserts
            if len(create) > 1000:
                MetricFuture.objects.using(db_alias).bulk_create(create)
                create = []

        # Create new object
        if current is None:
            current = MetricFuture(
                date=metric.date,
                scope=metric.scope,
                relation=metric.relation,
                secondary=metric.secondary,
                data=[],
            )
            current_data = {}

        # Inject value
        current_data[metric.kind] = metric.value

    if create:
        MetricFuture.objects.using(db_alias).bulk_create(create)
    print(".", flush=True)  # noqa: T201


class Migration(migrations.Migration):
    dependencies = [
        ("metrics", "0014_metricfuture"),
    ]

    operations = [
        migrations.RunPython(migrate_metrics, migrations.RunPython.noop, elidable=True)
    ]
