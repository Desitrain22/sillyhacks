# Generated by Django 5.0.3 on 2024-04-01 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dasite", "0002_rename_room_id_user_room"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tacoentryevent",
            name="status",
            field=models.IntegerField(default=1),
        ),
    ]
