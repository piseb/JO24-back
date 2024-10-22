from django.contrib import admin
from django.contrib import admin

from api import models


class DisciplineAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class EventAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "begin_at", "end_at"]
    date_hierarchy = "begin_at"


class OfferAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "price", "disable"]
    list_filter = ["disable"]


admin.site.register(models.Discipline, DisciplineAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Offer, OfferAdmin)
