from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(to=User, through="DocumentPermission")

    def __str__(self):
        return f"{self.title}"


class UserAccessDetail(models.Model):
    READ_ONLY = "RO"
    EDIT = "ED"
    PERMISSION_CHOICES = {READ_ONLY: "Read Only", EDIT: "Edit"}
    document = models.ForeignKey(to=Document, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    permission_type = models.CharField(
        max_length=2, choices=PERMISSION_CHOICES, default=EDIT
    )

    class Meta:
        # Ensure each user has only one permission per document
        unique_together = ("document", "user")
