# Generated by Django 3.2.14 on 2022-09-07 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_offer_is_posted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='item',
            new_name='bestselling_item',
        ),
    ]