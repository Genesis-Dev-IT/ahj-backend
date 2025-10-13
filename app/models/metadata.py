from django.db import models
from django.db.models import Q


class ReferenceCodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "reference_codes"
 
    def __str__(self):
        return self.type


class PermitType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=50, db_index=True)
    

    class Meta:
        db_table = "permit_type"
        constraints = [
            models.CheckConstraint(
                check=Q(type__in=["construction", "electrical", "building", "fire"]),
                name="permit_type_valid",
            ),
        ]
 
    def __str__(self):
        return self.type

class StandardLabels(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    always_required = models.BooleanField(default=False)

    class Meta:
        db_table = "standard_labels"

    def __str__(self):
        return self.name

# class RequirementReferenceCodeMapping(models.Model):
#     REQUIREMENT_TYPE = [
#         ("electrical_requirement", "Electrical Requirement"),
#         ("structural_requirement", "Structural Requirement"),
#         ("fire", "Fire Requirement"),
#     ]

#     id = models.BigAutoField(primary_key=True)
#     reference_code = models.ForeignKey(ReferenceCodes, on_delete=models.CASCADE, related_name="requirement_mappings")
#     type = models.CharField(max_length=50, choices=REQUIREMENT_TYPE)
#     data = models.JSONField(default=dict, blank=True, null=True)

#     class Meta:
#         db_table = "requirement_reference_code_mapping"

#     def __str__(self):
#         return f"{self.type} → RefCode {self.reference_code.code if self.reference_code else 'N/A'}"

