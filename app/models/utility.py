from django.db import models
from genesis.utils import current_timestamp
from app.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Utility(models.Model):
    LEVEL_CHOICES = [
        ('city', 'City'),
        ('township', 'Township'),
        ('state', 'State'),
        ('country', 'Country'),
    ]

    TYPE_CHOICES = [
        ('gas', 'Gas'),
        ('solar', 'Solar'),
        ('sewer', 'Sewer'),
        ('electric', 'Electric'),
        ('water', 'Water'),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=10, blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    website_link = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="utility_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="utility_updated")

    class Meta:
        db_table = "utility"
        constraints = [
            models.CheckConstraint(
                check=models.Q(level__in=['city', 'township', 'state', 'country']),
                name="utility_level_valid"
            ),
            models.CheckConstraint(
                check=models.Q(type__in=['gas', 'solar', 'sewer', 'electric', 'water']),
                name="utility_type_valid"
            ),
        ]
    
    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()  # Update timestamp on every save
        super().save(*args, **kwargs)  # Call the default save method

    def __str__(self):
        return self.name

class ProjectLevel(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = "project_level"

    def __str__(self):
        return f"{self.name} ({self.code})"


class SolarUtility(models.Model):
    SUBMISSION_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    id = models.BigAutoField(primary_key=True)
    utility = models.ForeignKey(
        Utility, on_delete=models.CASCADE, related_name="solar_utilities"
    )
    website_link = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    submission_process = models.CharField(max_length=10, choices=SUBMISSION_CHOICES)
    offset = models.DecimalField(
        max_digits=5,      # allows up to 100.00
        decimal_places=2,  # supports decimals like 99.99
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text="Offset percentage (0-100, decimals allowed)."
    )
    review_days_part1 = models.IntegerField(blank=True, null=True)
    review_days_part2 = models.IntegerField(blank=True, null=True)
    application_submission_link_part1 = models.TextField(blank=True, null=True)
    application_submission_link_part2 = models.TextField(blank=True, null=True)
    requires_combined_pdf = models.BooleanField(default=False)
    project_level = models.ForeignKey(ProjectLevel, on_delete=models.CASCADE)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "solar_utility"
        constraints = [
            models.CheckConstraint(
                check=models.Q(submission_process__in=['online', 'offline']),
                name="solar_submission_valid"
            ),
        ]
    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()  # Update timestamp on every save
        super().save(*args, **kwargs)  # Call the default save method
    
    def __str__(self):
        return f"Solar Utility ({self.utility.name})"


class SolarUtilityPart1Requirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    solar_utility = models.OneToOneField(
        SolarUtility, on_delete=models.CASCADE, related_name="part1_requirement"
    )

    part1_application_form = models.BooleanField(default=False)
    engineering_drawing = models.BooleanField(default=False)
    inverter_datasheet = models.BooleanField(default=False)
    pv_watts = models.BooleanField(default=False)
    change_of_contract_letter = models.BooleanField(default=True)  # always mandatory
    docusign_certificate = models.BooleanField(default=True)       # always mandatory
    load_calculation_direct = models.BooleanField(default=False)
    load_calculation_pe_stamped = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "solar_utility_part1_requirement"
    
    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()  # Update timestamp on every save
        super().save(*args, **kwargs)  # Call the default save method

    def __str__(self):
        return f"Part1 Requirements ({self.utility.name})"


class SolarUtilityPart2Requirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    solar_utility = models.OneToOneField(
        SolarUtility, on_delete=models.CASCADE, related_name="part2_requirement"
    )

    certificate_of_approval = models.BooleanField(default=False)
    part2_application_form = models.BooleanField(default=False)
    as_built = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "solar_utility_part2_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()  # Update timestamp on every save
        super().save(*args, **kwargs)  # Call the default save method

    def __str__(self):
        return f"Part2 Requirements ({self.utility.name})"
    
class ZipcodeUtilityMapping(models.Model):
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=20, db_index=True)
    
    class Meta:
        db_table = "zipcode_utility_mapping"
        constraints = [
            models.UniqueConstraint(fields=["zipcode", "utility"], name="unique_zipcode_utility")
        ]
        indexes = [
            models.Index(fields=["zipcode", "utility"]),
        ]