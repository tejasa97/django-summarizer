from django.contrib import admin
from .models import SummarizerTask, Summary


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(SummarizerTask)
class SummarizerTaskAdmin(admin.ModelAdmin):
    pass
