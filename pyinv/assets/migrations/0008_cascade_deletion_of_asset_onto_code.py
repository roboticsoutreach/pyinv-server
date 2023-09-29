# Generated by Django 3.2.14 on 2022-07-14 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_add_asset_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetcode',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.asset'),
        ),
    ]