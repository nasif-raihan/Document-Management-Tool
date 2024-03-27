from django.contrib import admin
from .models import Document, UserAccessDetail


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "created_at",
        "modified_at",
        "owner",
    )


@admin.register(UserAccessDetail)
class UserAccessDetailAdmin(admin.ModelAdmin):
    list_display = ("document", "user", "permission_type")
