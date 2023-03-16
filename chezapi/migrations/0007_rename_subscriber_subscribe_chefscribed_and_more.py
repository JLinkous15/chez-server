# Generated by Django 4.1.7 on 2023-03-15 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chezapi', '0006_alter_subscribe_chef_alter_subscribe_subscriber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscribe',
            old_name='subscriber',
            new_name='chefscribed',
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='chef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_chef', to='chezapi.chef'),
        ),
    ]
