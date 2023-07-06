# Generated by Django 4.2.3 on 2023-07-06 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('email', models.EmailField(default=0, max_length=254, verbose_name='Email')),
                ('phone', models.IntegerField(verbose_name='Phone')),
                ('bio', models.TextField(max_length=500, verbose_name='Bio')),
                ('image', models.CharField(max_length=300, verbose_name='Image')),
                ('timestamp', models.DateField(auto_now_add=True, verbose_name='user-created')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]