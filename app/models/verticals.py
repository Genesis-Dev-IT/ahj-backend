from django.db import models
from genesis.utils import current_timestamp
from app.models import User


class Vertical(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "verticals"

    def __str__(self):
        return self.name


class RequirementBlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "requirement_blocks"

    def __str__(self):
        return self.name


class VerticalBlockMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    vertical = models.ForeignKey(Vertical, on_delete=models.CASCADE, related_name="block_mappings")
    requirement_block = models.ForeignKey(RequirementBlock, on_delete=models.CASCADE, related_name="vertical_mappings")

    class Meta:
        db_table = "vertical_block_mapping"
        unique_together = ("vertical", "requirement_block")

    def __str__(self):
        return f"{self.vertical.name} -> {self.requirement_block.name}"
