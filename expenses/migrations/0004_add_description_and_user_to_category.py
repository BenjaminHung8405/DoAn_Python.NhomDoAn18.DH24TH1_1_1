from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0003_alter_user_date_joined_alter_user_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
