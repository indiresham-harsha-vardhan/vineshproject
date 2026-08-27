from django.db import models


class ChatConversation(models.Model):

    name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return f"{self.name} - {self.phone}"


class ChatMessage(models.Model):

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    message = models.TextField()

    sender = models.CharField(
        max_length=20,
        choices=[
            ("visitor", "Visitor"),
            ("admin", "Admin"),
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.message[:50]