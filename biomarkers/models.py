from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class BiomarkerCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20)
    
    # Reference ranges (medical/standard ranges)
    reference_range_min = models.FloatField(null=True, blank=True)
    reference_range_max = models.FloatField(null=True, blank=True)
    
    # Default target value and acceptable range for the biomarker
    default_target_value = models.FloatField(
        null=True, 
        blank=True,
        help_text="Default target value for this biomarker"
    )
    default_acceptable_range = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Default acceptable deviation from target value (±)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Biomarker Categories"

    def __str__(self):
        return self.name

    def is_value_within_reference_range(self, value):
        """Check if a value is within the medical reference range"""
        if self.reference_range_min is not None and value < self.reference_range_min:
            return False
        if self.reference_range_max is not None and value > self.reference_range_max:
            return False
        return True

class UserBiomarkerTarget(models.Model):
    """Personal targets and acceptable ranges for each user and biomarker"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BiomarkerCategory, on_delete=models.CASCADE)
    target_value = models.FloatField(
        help_text="Your target value for this biomarker"
    )
    acceptable_range = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Acceptable deviation from target value (±)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'category']

    def __str__(self):
        return f"{self.user.username}'s target for {self.category.name}"

    def is_value_within_target_range(self, value):
        """Check if a value is within the acceptable range of the target"""
        return abs(value - self.target_value) <= self.acceptable_range

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
    def is_within_reference_range(self):
        """Check if the value is within the medical reference range"""
        return self.category.is_value_within_reference_range(self.value)

    @property
    def is_within_target_range(self):
        """Check if the value is within the user's target range"""
        try:
            target = UserBiomarkerTarget.objects.get(
                user=self.user,
                category=self.category
            )
            return target.is_value_within_target_range(self.value)
        except UserBiomarkerTarget.DoesNotExist:
            # If no personal target is set, check against default target if available
            if (self.category.default_target_value is not None and 
                self.category.default_acceptable_range is not None):
                return abs(self.value - self.category.default_target_value) <= self.category.default_acceptable_range
            return None  # No target set