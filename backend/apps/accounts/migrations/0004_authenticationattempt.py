from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0003_bio_max_length")]
    operations = [
        migrations.CreateModel(
            name="AuthenticationAttempt",
            fields=[
                ("identity", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("request_times", models.JSONField(default=list)),
                ("failures", models.PositiveSmallIntegerField(default=0)),
                ("locked_until", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
    ]
