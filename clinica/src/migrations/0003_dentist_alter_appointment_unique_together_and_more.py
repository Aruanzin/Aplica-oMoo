# Generated by Django 5.1.4 on 2024-12-16 15:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_appointment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dentist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='appointment',
            name='dentist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='src.dentist'),
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('dentist', 'date_time')},
        ),
    ]
