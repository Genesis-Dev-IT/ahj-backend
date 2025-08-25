from django.db import models
from django.core.exceptions import ValidationError
from genesis.utils import current_timestamp

def validate_admin_email(user):
    """
    Custom validator to enforce that if a user is admin,
    their email must end with @genesisdesign.io
    """
    if user.is_admin and not user.email.endswith("@genesisdesign.io"):
        raise ValidationError("Admin users must have an @genesisdesign.io email address.")

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "user"

    def clean(self):
        validate_admin_email(self)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
