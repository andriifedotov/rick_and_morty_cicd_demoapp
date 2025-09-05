from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Character",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("status", models.CharField(max_length=50)),
                ("species", models.CharField(max_length=50)),
                ("type", models.CharField(blank=True, max_length=255)),
                ("gender", models.CharField(blank=True, max_length=50)),
                ("origin_name", models.CharField(blank=True, max_length=255)),
                ("origin_url", models.URLField(blank=True, max_length=500)),
                ("location_name", models.CharField(blank=True, max_length=255)),
                ("location_url", models.URLField(blank=True, max_length=500)),
                ("image", models.URLField(blank=True, max_length=500)),
                ("url", models.URLField(max_length=500)),
                ("created", models.DateTimeField()),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.AddIndex(
            model_name="character",
            index=models.Index(fields=["name"], name="characters_name_idx"),
        ),
        migrations.AddIndex(
            model_name="character",
            index=models.Index(fields=["species", "status"], name="characters_species_status_idx"),
        ),
        migrations.AddIndex(
            model_name="character",
            index=models.Index(fields=["origin_name"], name="characters_origin_idx"),
        ),
    ]

