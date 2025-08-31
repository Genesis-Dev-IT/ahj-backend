from django.db import models
from genesis.utils import current_timestamp
from app.models import User
from django.db.models import Q
from .state import State, StateSpecificInformation

class AHJ(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, db_index=True)  # City/Twp, State, County 
    state_code = models.CharField(max_length=10, null=True)
    # state = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, default="USA")
    building_code = models.CharField(max_length=100, blank=True, null=True)
    # state_specific_ic = models.ForeignKey(StateSpecificInformation, on_delete=models.CASCADE)
    nec_code = models.CharField(max_length=100, blank=True, null=True)
    nfpa_code = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ahj_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ahj_updated")

    class Meta:
        db_table = "ahj"
        constraints = [
            models.CheckConstraint(
                check=Q(type__in=["city", "twp", "state", "county", "other"]),
                name="location_type_valid",
            ),
        ]

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()  # Update timestamp on every save
        super().save(*args, **kwargs)  # Call the default save method

    def __str__(self):
        return self.name


class AHJRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey( AHJ, on_delete=models.CASCADE)
    pv_meter_required = models.BooleanField(default=False)
    ac_disconnect_required = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Requirement for {self.ahj.name} (ID: {self.id})"
    


class AHJSpecificRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    max_panel_system_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loading_calculation_threshold = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  #per square foot
    wind_speed = models.DecimalField( max_digits=6, decimal_places=2, null=True, blank=True)
    exposure_category = models.CharField(max_length=2, null=True, blank=True, help_text="ASCE 7 exposure category")
    snow_load = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Ground snow load in psf")
    ground_mount_allowed = models.BooleanField(default=False, help_text="Whether AHJ allows ground-mount systems")
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_specific_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Specific Requirement for {self.ahj.name} (ID: {self.id})"
    

class AHJElectricalRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    stamp_required = models.BooleanField(default=False, help_text="Does electrical work require an engineer stamp?")
    ee_stamp_for_main_breaker_derate = models.BooleanField(default=False)
    pv_meter_required = models.BooleanField(default=False)
    ac_disconnect_type = models.CharField(max_length=20, null=True, blank=True) # fused, non-fused 
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_electrical_requirement"
        constraints = [
            models.CheckConstraint(
                check=Q(ac_disconnect_type__in=["fused", "non-fused"]),
                name="ac_disconnect_type_valid",
            ),
        ]

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Electrical Requirement for {self.ahj.name} (ID: {self.id})"
    
class AHJStructuralSetbackRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    stamp_required = models.BooleanField(default=False, help_text="Does structural work require an engineer stamp?")
    fire_setback_distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Fire setback in feet (if specified)")
    fire_setback_code_year = models.IntegerField(null=True, blank=True, help_text="Year of fire code used for determining setback") 
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_structural_setback_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Structural Setback Requirement for {self.ahj.name} (ID: {self.id})"
    
class AHJGroundMountRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    
    soil_class = models.CharField(null=True, max_length=20, help_text="Soil classification")  #clay, gravel, rock
    freeze_depth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Maximum freeze depth in feet")
    thaw_depth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Depth to which soil thaws in feet")
    setback_front = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Front yard setback in feet")
    setback_back = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Back yard setback in feet")
    setback_side = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Side yard setback in feet")
    gm_max_height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Maximum height of ground-mounted solar in feet")

    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_ground_mount_requirement"
        constraints = [
            models.CheckConstraint(
                check=Q(soil_class__in=["clay", "gravel", "rock"]),
                name="soil_class_type_valid",
            ),
        ]

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ground Mount Requirement for {self.ahj.name} (ID: {self.id})"
    
class ZipcodeAHJMapping(models.Model):
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=20, db_index=True)
    class Meta:
        db_table = "zipcode_ahj_mapping"
        constraints = [
            models.UniqueConstraint(fields=["zipcode", "ahj"], name="unique_zipcode_ahj")
        ]
        indexes = [
            models.Index(fields=["zipcode", "ahj"]),
        ]