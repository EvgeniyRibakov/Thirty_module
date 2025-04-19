# Generated by Django 5.2 on 2025-04-19 09:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_alter_course_options_alter_lesson_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': [('can_view_course', 'Can view course'), ('can_edit_course', 'Can edit course'), ('can_delete_course', 'Can delete course')]},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'permissions': [('can_view_lesson', 'Can view lesson'), ('can_edit_lesson', 'Can edit lesson'), ('can_delete_lesson', 'Can delete lesson')]},
        ),
        migrations.RemoveField(
            model_name='course',
            name='preview',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='preview',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='video_url',
        ),
        migrations.AddField(
            model_name='lesson',
            name='video_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='lms.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
    ]
