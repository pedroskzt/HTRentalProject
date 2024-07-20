# Generated by Django 4.2.13 on 2024-07-20 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('tool_id', models.AutoField(primary_key=True, serialize=False)),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ToolsCategory',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ToolsModel',
            fields=[
                ('tools_model_id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('description', models.TextField(null=True)),
                ('image_name', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.toolscategory')),
            ],
            options={
                'unique_together': {('brand', 'model')},
            },
        ),
        migrations.CreateModel(
            name='ToolsHistory',
            fields=[
                ('tools_history_id', models.AutoField(primary_key=True, serialize=False)),
                ('rent_start_date', models.DateTimeField()),
                ('rent_end_date', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tools')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tools',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.toolsmodel'),
        ),
    ]
