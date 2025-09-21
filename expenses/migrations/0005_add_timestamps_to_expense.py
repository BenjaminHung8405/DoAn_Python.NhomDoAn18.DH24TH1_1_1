import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0004_add_description_and_user_to_category"),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
