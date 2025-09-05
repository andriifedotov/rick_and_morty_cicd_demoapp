from django.db import models

class Character(models.Model):
    id = models.IntegerField(primary_key=True)  # mirrors external ID
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    type = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    origin_name = models.CharField(max_length=255, blank=True)
    origin_url = models.URLField(max_length=500, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    location_url = models.URLField(max_length=500, blank=True)
    image = models.URLField(max_length=500, blank=True)
    url = models.URLField(max_length=500)
    created = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["species", "status"]),
            models.Index(fields=["origin_name"]),
        ]
        ordering = ["id"]


    def __str__(self):
        return f"{self.id}: {self.name}"