# Generated by Django 5.1.4 on 2024-12-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0004_dentalplan_appointment_value_client_birt_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dentist',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
