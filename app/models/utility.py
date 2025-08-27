from django.db import models
from genesis.utils import current_timestamp
from app.models import User

class Utility(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    state_code = models.CharField(max_length=10, db_index=True)
    state = models.CharField(max_length=100)
    production_meter = models.BooleanField(null=True, blank=True)
    disconnect = models.BooleanField(null=True, blank=True)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="utility_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="utility_updated")

    class Meta:
        db_table = "utility"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()  # Update timestamp on every save
        super().save(*args, **kwargs)  # Call the default save method

    def __str__(self):
        return self.name


class UtilityRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)

    system_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    farm_system_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minimum_system_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    net_metering_required = models.BooleanField(default=False)
    bidirectional_meter_required = models.BooleanField(default=False)
    production_meter_required = models.BooleanField(default=False)
    production_meter_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    disconnect_placement = models.CharField(   #exterior_wall, interior_panel_room, meter_location, service_entrance, visible_from_street, other   
        max_length=255,     
        null=True,
        blank=True,
        help_text="Comma-separated values (e.g. 'exterior_wall, meter_location')"
    )
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "utility_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Utility Requirement for {self.utility.name} (ID: {self.id})"
    

class UtilityICApplicationRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    application_type = models.CharField(  # Type A, Type B, Type C
        max_length=50,
        null=True,
        blank=True,
        help_text="Utility-defined application type (e.g., Type A, Type B, Type C)"
    )
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "utility_ic_application_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Utility IC Application Requirement for {self.utility.name} (ID: {self.id})"
    

class UtilityData(models.Model):
    id = models.BigAutoField(primary_key=True)
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    lc_required = models.BooleanField(default=False)
    hoi_required = models.BooleanField(default=False)
    online_submission = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "utility_data"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Utility Data for {self.utility.name} (ID: {self.id})"



class UtilityProductionMeterRequirement(models.Model):
    id = models.BigAutoField(primary_key=True)
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    system_size_kw = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="System size in kW")
    location_notes = models.TextField(null=True, blank=True, help_text="Notes about placement/location of meter")
    distance_from_service_ft = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Distance from main service meter")
    prohibited_locations = models.TextField(null=True, blank=True, help_text="Any prohibited locations (e.g., patio/carport)")
    wiring_orientation = models.CharField(max_length=100, null=True, blank=True, help_text="Line/top = inverter, Load/bottom = utility")
    sequence_notes = models.TextField(null=True, blank=True, help_text="Sequence of devices (Inverter > AC Disconnect > PV Meter > Interconnection)")
    meter_model = models.CharField(max_length=50, null=True, blank=True, help_text="Model of PV meter (e.g., Milbank U4518-XL-W)")
    meter_amp_rating = models.PositiveIntegerField(null=True, blank=True, help_text="Amp rating (e.g., 200)")
    meter_size = models.CharField(max_length=50, null=True, blank=True, help_text='Physical size (e.g., 15.5"x11"x4.375")')
    meter_features = models.TextField(null=True, blank=True, help_text="Ringless, bypass lever, 5th jaw, SMART etc.")
    wire_size = models.CharField(max_length=50, null=True, blank=True, help_text="Wire sizes (#8 for 100A, #6 for 200A)")
    is_meter_optional = models.BooleanField(default=False, help_text="Is meter optional?")
    exempt_under_kw = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Exemption threshold in kW")
    smart_meter_required = models.BooleanField(default=False, help_text="Whether SMART meter labeling is required")
    access_requirements = models.TextField(null=True, blank=True, help_text="Accessibility requirements (keyless, 24/7, etc.)")
    notes = models.TextField(null=True, blank=True, help_text="Any additional utility notes")

    created_at = models.BigIntegerField(default=current_timestamp)
    updated_at = models.BigIntegerField(default=current_timestamp)

    class Meta:
        db_table = "utility_production_meter_requirement"

    def save(self, *args, **kwargs):
        """Update 'updated_at' every time the object is saved."""
        self.updated_at = current_timestamp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Utility Production Meter Requirement for {self.utility.name} (ID: {self.id})"
    

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