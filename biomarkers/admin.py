from django.contrib import admin
from .models import BiomarkerCategory, BiomarkerRecord

@admin.register(BiomarkerCategory)
class BiomarkerCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'reference_range_min', 'reference_range_max')
    search_fields = ('name', 'description')

@admin.register(BiomarkerRecord)
class BiomarkerRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'value', 'date_recorded')
    list_filter = ('user', 'category', 'date_recorded')
    search_fields = ('notes',)