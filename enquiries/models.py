from django.db import models

from properties.models import Property


class Enquiry(models.Model):

    ENQUIRY_TYPE_CHOICES = [
        ("property", "Property Enquiry"),
        ("general", "General Enquiry"),
        ("callback", "Request Callback"),
        ("visit", "Property Visit"),
        ("home_loan", "Home Loan"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20
    )

    enquiry_type = models.CharField(
        max_length=30,
        choices=ENQUIRY_TYPE_CHOICES,
        default="property"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enquiries"
    )

    message = models.TextField(
        blank=True
    )

    preferred_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="new"
    )

    admin_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.name} - {self.phone}"

class VisitorEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email