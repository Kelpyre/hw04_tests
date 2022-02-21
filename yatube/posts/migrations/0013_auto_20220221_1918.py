# Generated by Django 2.2.9 on 2022-02-21 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Текст нового комментария', verbose_name='Текст комментария'),
        ),
    ]