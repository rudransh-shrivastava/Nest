# Generated by Django 5.2.3 on 2025-06-29 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("github", "0030_alter_organization_is_owasp_related_organization"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repository",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="repositories",
                to="github.organization",
                verbose_name="Organization",
            ),
        ),
    ]
