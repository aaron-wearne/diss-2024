# Generated by Django 4.2.10 on 2024-07-11 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0007_userprofile_following'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='notifcation_type',
            new_name='notification_type',
        ),
        migrations.AlterField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_from', to=settings.AUTH_USER_MODEL),
        ),
    ]