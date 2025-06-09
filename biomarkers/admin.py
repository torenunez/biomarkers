from django.contrib import admin
from .models import BiomarkerCategory, BiomarkerRecord, UserBiomarkerTarget

@admin.register(BiomarkerCategory)
class BiomarkerCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'unit', 
        'reference_range_min', 
        'reference_range_max',
        'default_target_value',
        'default_acceptable_range'
    )
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'unit')
        }),
        ('Reference Ranges', {
            'fields': ('reference_range_min', 'reference_range_max'),
            'description': 'Medical/standard reference ranges for this biomarker'
        }),
        ('Default Targets', {
            'fields': ('default_target_value', 'default_acceptable_range'),
            'description': 'Default target values that users can customize'
        })
    )

@admin.register(UserBiomarkerTarget)
class UserBiomarkerTargetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'target_value', 'acceptable_range')
    list_filter = ('user', 'category')
    search_fields = ('user__username', 'category__name')

@admin.register(BiomarkerRecord)
class BiomarkerRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'category',
        'value',
        'date_recorded',
        'is_within_reference_range',
        'is_within_target_range'
    )
    list_filter = ('user', 'category', 'date_recorded')
    search_fields = ('notes', 'user__username', 'category__name')
    readonly_fields = ('is_within_reference_range', 'is_within_target_range')