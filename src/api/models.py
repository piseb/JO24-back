import uuid

from django.db import models
from django.forms import ValidationError


class Discipline(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Event(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, blank=False, unique=True)
    begin_at = models.DateField(blank=False)
    end_at = models.DateField(blank=False)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if str(self.end_at) < str(self.begin_at):
            raise ValidationError({"end_at": "end_at must be equal or after begin_at"})

    def __str__(self) -> str:
        return f"{self.title} ({self.begin_at}/{self.end_at}): {self.description[:5]}"
