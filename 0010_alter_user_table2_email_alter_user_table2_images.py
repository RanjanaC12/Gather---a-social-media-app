# Generated by Django 4.1.7 on 2023-02-21 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0009_alter_user_table2_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_table2",
            name="email",
            field=models.CharField(
                max_length=255, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="user_table2",
            name="images",
            field=models.ImageField(upload_to="images"),
        ),
    ]
