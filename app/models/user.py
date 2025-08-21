from django.db import models
from genesis.utils import current_timestamp

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    password_hash = models.TextField()
    created_on = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email