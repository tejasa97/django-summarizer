from django.contrib import admin

# Register your models here.
from .models import SummarizerTask, Summary


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(SummarizerTask)
class SummarizerTaskAdmin(admin.ModelAdmin):
    pass
