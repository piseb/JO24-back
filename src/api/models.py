import uuid
from decimal import Decimal

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


class Offer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    ntickets = models.PositiveSmallIntegerField(blank=False)
    disable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        # adding 0 after decimal if need (10.1 -> 10.10 and 10 -> 10.00)
        self.price = format(Decimal(self.price), ".2f")
        if self.ntickets == 0:
            raise ValidationError({"ntickets": "at least 1 ticket"})

    def __str__(self) -> str:
        resp = f"{self.title} ({self.price}€ / {self.ntickets} tickets): {self.description[:5]}"
        if self.disable:
            return "DISABLE: " + resp
        return resp
