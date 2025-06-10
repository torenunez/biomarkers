from django.contrib import admin
from .models import BiomarkerCategory, BiomarkerRecord

@admin.register(BiomarkerCategory)
class BiomarkerCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'unit', 
        'reference_range_min', 
        'reference_range_max',
        'target_value'
    )
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'unit')
        }),
        ('Ranges and Targets', {
            'fields': ('reference_range_min', 'reference_range_max', 'target_value'),
            'description': 'Reference ranges indicate normal/healthy ranges. Target value is optional and must be within range.'
        })
    )

@admin.register(BiomarkerRecord)
class BiomarkerRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'category',
        'value',
        'date_recorded',
        'status'
    )
    list_filter = ('user', 'category', 'date_recorded')
    search_fields = ('notes', 'user__username', 'category__name')
    readonly_fields = ('status',)