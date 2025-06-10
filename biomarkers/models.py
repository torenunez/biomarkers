from django.db import models
from django.contrib.auth.models import User

class BiomarkerCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20)
    
    # Reference ranges (medical/standard ranges)
    reference_range_min = models.FloatField(null=True, blank=True)
    reference_range_max = models.FloatField(null=True, blank=True)
    
    # Optional target value for this biomarker
    target_value = models.FloatField(
        null=True, 
        blank=True,
        help_text="Optional target value for this biomarker (within reference range)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Biomarker Categories"

    def __str__(self):
        return self.name

    def is_value_within_range(self, value):
        """Check if a value is within the reference range"""
        if self.reference_range_min is not None and value < self.reference_range_min:
            return False
        if self.reference_range_max is not None and value > self.reference_range_max:
            return False
        return True

    def clean(self):
        """Validate that target_value is within reference range if provided"""
        from django.core.exceptions import ValidationError
        
        if self.target_value is not None:
            if self.reference_range_min is not None and self.target_value < self.reference_range_min:
                raise ValidationError("Target value must be within reference range")
            if self.reference_range_max is not None and self.target_value > self.reference_range_max:
                raise ValidationError("Target value must be within reference range")

class BiomarkerRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BiomarkerCategory, on_delete=models.CASCADE)
    value = models.FloatField()
    date_recorded = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.category.name}: {self.value} {self.category.unit} ({self.date_recorded.date()})"

    @property
    def is_within_range(self):
        """Check if the value is within the reference range"""
        return self.category.is_value_within_range(self.value)

    @property
    def status(self):
        """Return the status of this measurement"""
        if not self.is_within_range:
            if self.value < self.category.reference_range_min:
                return "Below Range"
            return "Above Range"
        
        # If there's a target value, indicate if we're at/above/below target
        if self.category.target_value is not None:
            if self.value == self.category.target_value:
                return "At Target"
            elif self.value < self.category.target_value:
                return "Below Target"
            return "Above Target"
        
        return "Within Range"