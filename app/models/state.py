from django.db import models

class State(models.Model):
    id = models.BigIntegerField(primary_key=True)
    abbr = models.CharField(max_length=10, db_index=True)  # e.g. "AZ"
    country = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "state"

class StateSpecificInformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="specific_information"
    )
    state_specific_ic_code = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "state_specific_information"