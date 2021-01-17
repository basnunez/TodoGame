# Generated by Django 3.0.5 on 2020-11-22 21:08

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20201122_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game_detail',
            name='fk_juego',
        ),
        migrations.AddField(
            model_name='game',
            name='desc',
            field=ckeditor.fields.RichTextField(default='null', verbose_name='Descripcion'),
        ),
        migrations.AddField(
            model_name='game',
            name='link_imagen',
            field=models.TextField(default='null'),
        ),
    ]
