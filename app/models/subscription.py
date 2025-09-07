from django.db import models
from genesis.utils import current_timestamp
from app.models import User
from django.db.models import Q
import uuid
from datetime import timedelta

class SubscriptionPlan(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(
        max_length=50,
        unique=True,
        help_text="Plan type (e.g., trial, basic, premium)"
    )
    limit = models.PositiveIntegerField(help_text="Usage limit for this plan")
    validity_days = models.PositiveIntegerField(default=30, help_text="Number of days the plan is valid")

    class Meta:
        db_table = "subscription_plan"
    
    def __str__(self):
        return f"{self.type.capitalize()} (Limit: {self.limit}, Validity: {self.validity_days} days)"
    
class UserSubscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name="subscriptions")
    active = models.BooleanField(default=True)
    expires_at = models.BigIntegerField(default=current_timestamp)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "user_subscription"
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(active=True),
                name="one_active_subscription_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.plan.type} ({'active' if self.active else 'inactive'})"


class ApiToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="api_token")
    # plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name="api_token")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    limit = models.PositiveIntegerField(default=0)
    expires_at = models.BigIntegerField()
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_token")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_token")
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "api_token"
        constraints = [
            # One active token per user
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(active=True),
                name="one_active_token_per_user"
            )
        ]
    
    def save(self, *args, **kwargs):
        # """Auto set expires_at = created_at + 30 days on first save."""
        if not self.expires_at:    # only set if its missing while saving 
            # 30 days in milliseconds
            thirty_days_ms = int(timedelta(days=30).total_seconds() * 1000)
            self.expires_at = current_timestamp() + thirty_days_ms

        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token {self.token} (User: {self.user}, Active: {self.active})"
    

class ApiUsage(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="api_usage")
    api_name = models.CharField(max_length=100, help_text="Name of the API called")
    data_id = models.BigIntegerField(null=True, blank=True, help_text="Optional resource identifier (e.g., ahj_id, utility_id)")
    created_at = models.BigIntegerField(default=current_timestamp)
    
    class Meta:
        db_table = "api_usage"
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self):
        return f"{self.user} called {self.api_name} at {self.created_at}"