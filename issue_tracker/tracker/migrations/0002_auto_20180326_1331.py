# Generated by Django 2.0.3 on 2018-03-26 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issue_issue_assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='state',
            field=models.CharField(choices=[('U', 'Unassigned'), ('A', 'Assigned'), ('P', 'In progress'), ('D', 'Done')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='issue_issue_created', to=settings.AUTH_USER_MODEL),
        ),
    ]