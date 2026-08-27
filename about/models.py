from django.db import models


class AboutUs(models.Model):

    company_name = models.CharField(
        max_length=200
    )

    tagline = models.CharField(
        max_length=300,
        blank=True
    )

    heading = models.CharField(
        max_length=300
    )

    description = models.TextField()

    mission = models.TextField(
        blank=True
    )

    vision = models.TextField(
        blank=True
    )

    experience = models.CharField(
        max_length=100,
        blank=True
    )

    properties_count = models.CharField(
        max_length=100,
        blank=True
    )

    happy_clients = models.CharField(
        max_length=100,
        blank=True
    )

    image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.company_name