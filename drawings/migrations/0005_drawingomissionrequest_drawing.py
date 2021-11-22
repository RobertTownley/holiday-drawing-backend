# Generated by Django 3.2.9 on 2021-11-22 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drawings', '0004_remove_participant_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawingomissionrequest',
            name='drawing',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='omission_drawing', to='drawings.drawing'),
            preserve_default=False,
        ),
    ]