# Generated by Django 3.0.5 on 2020-04-14 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('readmybook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='college',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.CreateModel(
            name='requestBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('received', 'received'), ('returned', 'returned'), ('cancelled', 'cancelled')], default='pending', max_length=20)),
                ('by_status', models.CharField(choices=[('pending', 'pending'), ('done', 'done')], default='pending', max_length=20)),
                ('to_status', models.CharField(choices=[('pending', 'pending'), ('done', 'done')], default='pending', max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readmybook.BooksDB')),
                ('request_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_to', to=settings.AUTH_USER_MODEL)),
                ('request_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
