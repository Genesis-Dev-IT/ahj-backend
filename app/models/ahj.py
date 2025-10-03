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
    stamp_required = models.BooleanField(default=False, help_text="Does electrical work require an engineer stamp?")
    ee_stamp_for_main_breaker_derate = models.BooleanField(default=False)
    ee_stamp_for_main_breaker_derate_remarks = models.TextField(null=True, blank=True)
    pv_meter_required = models.BooleanField(default=False)
    pv_meter_required_remarks = models.TextField(null=True, blank=True)
    ac_disconnect_type = models.CharField(max_length=20, null=True, blank=True)  # fused, non-fused 
    ac_disconnect_type_remarks = models.TextField(null=True, blank=True)

    # New fields
    one_line_requirement = models.CharField(max_length=50, null=True, blank=True, help_text="One line / three line requirement for residential or commercial property.")
    data_sheets = models.CharField(max_length=255, null=True)
    conductor_sizing_and_ocp = models.TextField(null=True, blank=True, help_text="Conductor sizing and overcurrent protection.")

    # Rapid shutdown
    is_rsd_needed = models.BooleanField(default=False)
    rsd_requirement = models.TextField(null=True, blank=True, help_text="RSD should be next to inverter (AHJ specific requirement).")

    # Disconnects
    is_disconnect_required = models.BooleanField(default=False)
    disconnect_remarks = models.TextField(null=True, blank=True, help_text="Where disconnect is required (AHJ specific requirement).")

    # Grounding and bonding
    is_grounding_and_bonding_required = models.BooleanField(default=False)
    grounding_and_bonding_remarks = models.TextField(null=True, blank=True)

    electrical_panel_connection = models.TextField(null=True, blank=True, help_text="Electrical panel connection (The 120% Rule).")
    labeling = models.TextField(null=True, blank=True)

    # Loading calculation
    is_loading_calculation_required = models.BooleanField(default=False)
    loading_calculation_remarks = models.TextField(null=True, blank=True)

    wire_size_requirements = models.TextField(null=True, blank=True)
    production_meter_requirements = models.TextField(null=True, blank=True)
    power_line_filter_requirement = models.TextField(null=True, blank=True)
    recommended_ic = models.TextField(null=True, blank=True)
    utility_specific_note_of_eld = models.TextField(null=True, blank=True)
    electrical_stamping = models.TextField(null=True, blank=True)

    # Components
    service_panel = models.TextField(null=True, blank=True)
    interconnection_type = models.TextField(null=True, blank=True)
    conduit_type = models.TextField(null=True, blank=True)
    conduit_size = models.TextField(null=True, blank=True)
    utility_meter = models.TextField(null=True, blank=True)
    junction_box = models.TextField(null=True, blank=True)
    grounding = models.TextField(null=True, blank=True)
    main_service_panel = models.TextField(null=True, blank=True)
    spd_device = models.TextField(null=True, blank=True)
    grounding_electrode_conductor = models.TextField(null=True, blank=True)

    ahj_specific_notes = models.TextField(null=True, blank=True)

    # Placard
    placard_requirement_remarks = models.TextField(null=True, blank=True)

    ess_specific_requirements = models.TextField(null=True, blank=True)
    e_stop_button_requirement = models.TextField(null=True, blank=True)

    # 3-line diagram
    three_line_diagram_required = models.BooleanField(default=False)
    three_line_diagram_remarks = models.TextField(null=True, blank=True)

    certified_electrical_contractor = models.BooleanField(default=False)

    string_details = models.TextField(null=True, blank=True)

    rule_120_percent_required = models.BooleanField(default=False)

    # Timestamps
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
    SEAL_TYPE = [
         ("wet", "Wet"),
        ("digital", "Digital"),
    ]
    id = models.BigAutoField(primary_key=True)
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE)
    stamp_required = models.BooleanField(default=True, editable=False, help_text="Does structural work require an engineer stamp?")
    seal_type = models.CharField(max_length=10, choices=SEAL_TYPE, null=True, blank=True, help_text="Type of seal required (Wet or Digital)" )
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
    ahj = models.ForeignKey(AHJ, on_delete=models.CASCADE, related_name="safety_instructions")
    equipment_location_remarks = models.TextField(null=True, blank=True)
    roof_load_remarks = models.TextField(null=True, blank=True)

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
    flat_roof = models.BooleanField(default=False, help_text="Is the roof flat?")
    roof_condition = models.CharField(max_length=255, null=True, blank=True, help_text="Condition of the roof (e.g., good, needs repair, unknown)")
    structural_stamp_by_contractor = models.BooleanField(default=False, help_text="Is a structural stamp required by a certified contractor?")
    dead_load_requirement = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Dead load requirement in psf (pounds per square foot)")
    property_lines = models.TextField(null=True, blank=True, help_text="Details about property lines relevant to structural requirements")
    obstructions = models.TextField(null=True, blank=True, help_text="Notes on obstructions affecting structural requirements")

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

    
