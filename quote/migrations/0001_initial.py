# Generated by Django 3.0.5 on 2021-04-23 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('customer_first_name', models.CharField(max_length=50)),
                ('customer_last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=1000, unique=True)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('customer_phone_num', models.CharField(max_length=15)),
                ('materials', models.TextField(blank=True, null=True)),
                ('job_description', models.TextField()),
                ('date_of_job', models.DateField(blank=True, null=True)),
                ('removal_included', models.BooleanField(blank=True, default=False, null=True)),
                ('price_of_removal', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_of_materials', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_of_labour', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('quote_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sent_quote', models.BooleanField(blank=True, default=False, null=True)),
                ('associated_job', models.CharField(blank=True, max_length=25, null=True)),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
