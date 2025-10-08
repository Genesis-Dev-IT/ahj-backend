from django.db import models
from genesis.utils import current_timestamp
from app.models import User
from django.db.models import Q
from .state import State, StateSpecificInformation
from .metadata import (
    ReferenceCodes, PermitType 
)


class AHJ(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, db_index=True)  # City/Twp, State, County 
    parent_county = models.CharField(max_length=255, null=True)
    state_code = models.CharField(max_length=10, null=True)
    # state = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, default="USA")
    # state_specific_ic = models.ForeignKey(StateSpecificInformation, on_delete=models.CASCADE)
    website = models.CharField(max_length=255, null=True)
    data_source = models.CharField(max_length=255, null=True)
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


class AHJSolarRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    pv_meter_required = models.BooleanField(default=False)
    ac_disconnect_required = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_solar_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Requirement for {self.ahj.name} (ID: {self.id})"
    
class AHJRemark(models.Model):
    id = models.BigAutoField(primary_key=True)
    remark = models.TextField(null=True, blank=True)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ahj_remark_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ahj_remark_updated")
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "ahj_remarks"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Remark for AHJ (ID: {self.id}): {self.remark}"

class AHJElectricalRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)

    # PV meter
    pv_meter_required = models.BooleanField(default=False)
    pv_meter_required_remarks = models.TextField(null=True, blank=True)

    # Drawings & datasheets
    conductor_sizing_and_ocp = models.TextField(null=True, blank=True, help_text="Conductor sizing and overcurrent protection.")

    # Rapid Shutdown
    is_rsd_needed = models.BooleanField(default=False)
    rsd_requirement = models.TextField(null=True, blank=True, help_text="RSD should be next to inverter (AHJ specific requirement).")
    rsd_requirement_remarks = models.TextField(null=True, blank=True, help_text="RSD Requirement remarks.")

    # Disconnect requirements
    is_disconnect_required = models.BooleanField(default=False)
    disconnect_remarks = models.TextField(null=True, blank=True, help_text="Where disconnect is required (AHJ specific requirement).")

    # Panel, labeling & calculations
    is_loading_calculation_required = models.BooleanField(default=False)
    loading_calculation_remarks = models.TextField(null=True, blank=True)

    # Misc
    wire_size_requirements = models.TextField(null=True, blank=True)

    # Components
    interconnection_type = models.TextField(null=True, blank=True)
    min_conduit_size = models.TextField(null=True, blank=True)

    ess_disconect = models.BooleanField(default=False)
    ess_specific_requirements = models.TextField(null=True, blank=True)
    eld_requirement = models.BooleanField(default=False)
    eld_requirement_remarks = models.BooleanField(default=False)
    grounding_remarks = models.TextField(null=True, blank=True)

    electrical_requirements_notes = models.TextField(null=True, blank=True, help_text="Electrical Requirement Notes")

    # Timestamps
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_electrical_requirement"

    def save(self, *args, **kwargs):
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Electrical Requirement for {self.ahj.name} (ID: {self.id})"


# class AHJSetbackRequirement(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
#     fire_setback_distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Fire setback in feet (if specified)")
#     fire_setback_distance_remarks = models.TextField(blank=True, null= True)
#     created_at = models.BigIntegerField(default=current_timestamp)
#     updated_at = models.BigIntegerField(default=current_timestamp)

#     class Meta:
#         db_table = "ahj_setback_requirement"

#     def save(self, *args, **kwargs):
#         """Update 'updated_at' every time the object is saved."""
#         self.updated_at = current_timestamp()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Structural Setback Requirement for {self.ahj.name} (ID: {self.id})"
    
class AHJGroundMountRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    
    setback = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Minimum required setback distance in feet")
    setback_remarks = models.TextField(null=True, blank=True, help_text="Additional notes or remarks about setbacks")
    location_of_ground_mount = models.CharField(max_length=255, null=True, blank=True, help_text="Location description or zoning area for ground mount installation")

    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_ground_mount_requirement"

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

class AHJCodeMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="code_mappings")
    code = models.ForeignKey(ReferenceCodes, on_delete=models.CASCADE, related_name="ahj_mappings")

    class Meta:
        db_table = "ahj_code_mapping"
        unique_together = ("ahj", "code")

    def __str__(self):
        return f"{self.ahj} (ID: {self.id})"
    

class AHJPermitMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="permit_mappings")
    ahj_permit_type = models.ForeignKey(PermitType, on_delete=models.CASCADE, related_name="ahj_mappings")

    class Meta:
        db_table = "ahj_permit_mapping"
        unique_together = ("ahj", "ahj_permit_type")

    def __str__(self):
        return f"{self.ahj} -> {self.ahj_permit_type}"  

class AHJSafetyInstructions(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey( "AHJ", on_delete=models.CASCADE, related_name="safety_instructions")
    instructions =  models.TextField(blank=True, null=True, help_text="List of safety instructions for AHJ")

    class Meta:
        db_table = "ahj_safety_instructions"

    def __str__(self):
        return f"Safety Instructions for {self.ahj}"


class AHJLabel(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="labels")
    label_name = models.CharField(max_length=100)

    class Meta:
        db_table = "ahj_label"
        unique_together = ("ahj", "label_name")
        
    def __str__(self):
        return f"{self.label_name} ({self.ahj})"
    
class AHJEnvironmentalData(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="environmental_data")
    wind_speed = models.FloatField(null=True, blank=True)
    exposure_category = models.CharField(max_length=10, null=True, blank=True)
    snow_load = models.FloatField(null=True, blank=True)
    high_temp = models.FloatField(null=True, blank=True)
    min_temp = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "ahj_environmental_data"
        unique_together = ("ahj",)

    def __str__(self):
        return f"Environmental Data for {self.ahj}"
    

class AHJStructuralRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="structural_requirements")
    array_layout_required = models.BooleanField(default=False)
    array_layout_required_remarks = models.TextField(null=True, blank=True, help_text="Remarks of Aaray Layout.")
    property_plan_required = models.BooleanField(default=False)
    property_plan_required_remarks = models.TextField(null=True, blank=True, help_text="Remarks of Property Plan.")
    fire_setbacks = models.TextField(null=True, blank=True, help_text="Details about Fire Setbacks if any")
    
    roof_condition = models.CharField(max_length=255, null=True, blank=True, help_text="Condition of the roof (e.g., good, needs repair, unknown)")
    dead_load_requirement = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Dead load requirement in psf (pounds per square foot)") 
    max_panel_system_weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Maximum panel system weight in pounds per square foot (psf)")
    racking_realted_requirement = models.TextField(null=True, blank=True, help_text="Details about racking")
    framing_and_attic_details = models.TextField(null=True, blank=True, help_text="Details about Framing & Attic Details")
    wind_zone_representation_on_planset =  models.BooleanField(default=False)
    structural_requirements_notes = models.TextField(null=True, blank=True, help_text="Structural Requirement Notes")

    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_structural_requirement"
        unique_together = ("ahj",)

    def save(self, *args, **kwargs):
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Structural Requirement for {self.ahj.name} (ID: {self.id})"

   
class AHJRoofMountRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="roof_mount_requirements")
    permitted_zones = models.CharField(max_length=255, null=True, blank=True)
    roof_mount_requirements_notes = models.TextField(null=True, blank=True, help_text="Notes for Roof Mount Requirement.")
    #   height_restriction: {
    maximum_above_roof = models.CharField(max_length=255, null=True, blank=True)
    included_in_building_height = models.BooleanField(default=False)
    #   },
    #   installation_requirements: {
    roof_boundary_setback = models.CharField(max_length=255, null=True, blank=True)
    manual_shutoff_required = models.BooleanField(default=False)
    shutoff_location = models.CharField(max_length=255, null=True, blank=True)
    nec_placard_required = models.BooleanField(default=False)
    placard_location = models.CharField(max_length=255, null=True, blank=True)
    #   }
    #     #   restrictions: {
    front_yard = models.CharField(max_length=255, null=True, blank=True)
    #   }

    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_roof_mount_requirement"
        unique_together = ("ahj",)

    def save(self, *args, **kwargs):
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Roof Mount Requirement for {self.ahj.name} (ID: {self.id})"
    

# class AHJSolarFireRequirements(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="solar_fire_requirement")
#     fire_access = models.BooleanField(default=False, help_text="Is fire access required?")
#     other_ahj_specific_req = models.TextField(null=True, blank=True, help_text="Other AHJ-specific fire-related requirements")
#     evacuation_plan = models.BooleanField(default=False, help_text="Is evacuation plan required?")
#     rapid_shutdown_information = models.BooleanField(default=False, help_text="Is rapid shutdown information required?")
#     fire_code_setbacks = models.BooleanField(default=False, help_text="Are fire code setbacks required?")
#     location_of_disconnects = models.BooleanField(default=False, help_text="Location of disconnects required?")
#     fire_resistant_materials = models.BooleanField(default=False, help_text="Fire-resistant materials compliance required?")
#     battery_storage_compliance = models.BooleanField(default=False, help_text="Battery storage systems compliance required?")

#     created_at = models.BigIntegerField(default=current_timestamp)
#     updated_at = models.BigIntegerField(default=current_timestamp)

#     class Meta:
#         db_table = "ahj_solar_fire_requirement"
#         unique_together = ("ahj",)

#     def save(self, *args, **kwargs):
#         self.updated_at = current_timestamp()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Solar Fire Requirement for {self.ahj.name} (ID: {self.id})"

class AHJPermits(models.Model):
    SUBMISSION_METHOD = [("hard_copy", "Hard Copy"), ("online", "Online")]
    SEAL_TYPE = [
        ("wet", "Wet"),
        ("digital", "Digital"),
    ]

    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey("AHJ", on_delete=models.CASCADE, related_name="permits")

    construction_permit = models.BooleanField(default=False)
    construction_permit_form = models.CharField(max_length=255, null=True, blank=True, help_text="Link to Construction Permit form")
    electrical_permit = models.BooleanField(default=False)
    electrical_permit_form = models.CharField(max_length=255, null=True, blank=True, help_text="Link to Electrical Permit form")
    building_permit = models.BooleanField(default=False)
    building_permit_form = models.CharField(max_length=255, null=True, blank=True, help_text="Link to Building Permit form")
    fire_permit = models.BooleanField(default=False)
    fire_permit_form = models.CharField(max_length=255, null=True, blank=True, help_text="Link to Fire Permit form")

    zoning = models.BooleanField(default=False)
    zoning_remarks = models.TextField(blank=True, null=True)
    form_of_submission = models.CharField(max_length=20, choices=SUBMISSION_METHOD, null=True, blank=True, help_text="Form of submission (Hard copy / Online)")
    structural_and_electrical_stamp_on_planset = models.BooleanField(default=False)
    seal_type = models.CharField( max_length=10, choices=SEAL_TYPE, null=True, blank=True, help_text="Type of engineer seal required (Wet or Digital)")

    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "ahj_permits"
        constraints = [
            models.CheckConstraint(check=Q(form_of_submission__in=["hard_copy", "online"]) | Q(form_of_submission__isnull=True), name="valid_submission_method"),
        ]

    def save(self, *args, **kwargs):
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Permits for {self.ahj.name} (ID: {self.id})"

    
