import uuid

from django.db import models
from django.forms import ValidationError


class Discipline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if not self.name:
            raise ValidationError({"nom": "Le nom est obligatoire."})

    def __str__(self) -> str:
        return f"{self.name}"


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        # no empty string for fields:
        not_blank_tests = [
            (self.discipline, "discipline", "La discipline"),
            (self.title, "title", "Le titre"),
            (self.begin_at, "begin_at", "La date de début"),
            (self.end_at, "end_at", "La date de fin"),
            (self.description, "description", "La description"),
        ]
        for att, field, txt in not_blank_tests:
            if not att:
                raise ValidationError({field: f"{txt} est obligatoire."})

        if str(self.end_at) < str(self.begin_at):
            raise ValidationError(
                {
                    "end_at": "La date de fin doit être la même ou après la date de début."
                }
            )

    def __str__(self) -> str:
        return f"{self.title} ({self.begin_at}/{self.end_at}): {self.description[:5]}"
