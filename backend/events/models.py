from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    source = models.CharField(max_length=128, blank=True, null=True)
    url = models.URLField(max_length=1024, blank=True, null=True)
    uid = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} ({self.start_time.isoformat()})"


class ABTestVisit(models.Model):
    """Track A/B test visits and variant assignments"""
    session_key = models.CharField(max_length=128, db_index=True)
    variant = models.CharField(max_length=1, choices=[('A', 'Variant A'), ('B', 'Variant B')])
    visited_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    converted = models.BooleanField(default=False, help_text="Whether the user clicked the button")

    class Meta:
        ordering = ['-visited_at']

    def __str__(self):
        return f"Variant {self.variant} - {self.visited_at.isoformat()}"
