from django.db import models
from django.utils import timezone
from datetime import timedelta
from genesis.utils import current_timestamp

class PlanQuota(models.Model):
    PLAN_CHOICES = [
        ("trial", "Trial"),
        ("basic", "Basic"),
        ("premium", "Premium"),
    ]

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, primary_key=True)
    monthly_limit = models.PositiveIntegerField()

    class Meta:
        db_table = "plan_quota"

    def __str__(self):
        return f"{self.plan} ({self.monthly_limit} calls)"


class ApiToken(models.Model):
    PLAN_CHOICES = [
        ("trial", "Trial"),
        ("basic", "Basic"),
        ("premium", "Premium"),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tokens")
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    token_hash = models.TextField()
    max_calls = models.PositiveIntegerField()
    call_count = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    expires_at = models.BigIntegerField(default=current_timestamp)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "api_token"

    def __str__(self):
        return f"{self.user.email} - {self.plan} token"

    def save(self, *args, **kwargs):
        """Auto set expires_at = created_at + 30 days on first save."""
        if not self.id or not self.expires_at:
            # 30 days in milliseconds
            thirty_days_ms = int(timedelta(days=30).total_seconds() * 1000)
            self.expires_at = current_timestamp() + thirty_days_ms

        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """Check if token expired either by date or usage."""
        return (
            not self.active
            or current_timestamp() > self.expires_at
            or self.call_count >= self.max_calls
        )