from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save
from django.dispatch import receiver


def generate_unique_code(model):
    code = uuid.uuid4().hex[:6].upper()
    if not is_unique(code, model):
        generate_unique_code()
    return code

def is_unique(code, model):
    model_instance = apps.get_model('solargurus', model)
    results = model_instance.objects.filter(referral_code=code)
    if len(results) > 0:
        return False
    return True


@python_2_unicode_compatible
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return '{}-{}-{}'.format(
            self.id,
            self.user,
            self.type
        )


@python_2_unicode_compatible
class Area(models.Model):
    name = models.CharField(max_length=200)
    img = models.CharField(max_length=300, blank=True, null=True)
    zipcodes = ArrayField(models.CharField(max_length=200), blank=True)

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class EndUser(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'End User'
        verbose_name_plural = 'End Users'

    def __str__(self):
        return '{}: {}'.format(self.name, self.email)



@python_2_unicode_compatible
class RealEstateAgent(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    logo = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    referral_code = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Real Estate Agent'
        verbose_name_plural = 'Real Estate Agents'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # setattr(self, 'referral_code', generate_unique_code('RealEstateAgent'))
        super(RealEstateAgent, self).save(*args, **kwargs)

@receiver(pre_save, sender=RealEstateAgent)
def save_rea_referral_code(sender, instance, **kwargs):
    if instance.referral_code is None:
        print('setting referral_code')
        setattr(instance, 'referral_code', generate_unique_code('RealEstateAgent'))


@python_2_unicode_compatible
class Vendor(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    logo = models.CharField(max_length=300, blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)
    slogan = models.CharField(max_length=300, blank=True, null=True)
    accolades = models.CharField(max_length=500, blank=True, null=True)
    associations = models.CharField(max_length=1000, blank=True, null=True)
    certified = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EnergyAdvisor(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)
    logo = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    referral_code = models.CharField(max_length=200, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, blank=True, null=True)

    class Meta:
        verbose_name = 'Energy Advisor'
        verbose_name_plural = 'Energy Advisors'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # setattr(self, 'referral_code', generate_unique_code('EnergyAdvisor'))
        super(EnergyAdvisor, self).save(*args, **kwargs)


@receiver(pre_save, sender=EnergyAdvisor)
def save_ea_referral_code(sender, instance, **kwargs):
    if instance.referral_code is None:
        print('setting referral_code')
        setattr(instance, 'referral_code', generate_unique_code('EnergyAdvisor'))

@python_2_unicode_compatible
class PurchasingOptions(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'Purchasing Option'
        verbose_name_plural = 'Purchasing Options'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class StatusOptions(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'Status Option'
        verbose_name_plural = 'Status Options'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class LeadTypes(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'Lead Type'
        verbose_name_plural = 'Lead Types'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class LOI(models.Model):
    lead_source = models.ForeignKey(LeadTypes, blank=True, null=True)
    enduser = models.ForeignKey(EndUser)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    roof_material = models.CharField(max_length=200, blank=True, null=True)
    utility_provider = models.CharField(max_length=400)
    account_number = models.CharField(max_length=400, blank=True, null=True)
    payment_methods = models.ManyToManyField(PurchasingOptions, blank=True, null=True)
    meter_number = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=500, blank=True, null=True)
    signature = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'LOI'
        verbose_name_plural = 'LOIs'

    def __str__(self):
        return '{}: {}, {}, {} {}'.format(self.enduser.name, self.address, self.city, self.state, self.zipcode)


@python_2_unicode_compatible
class Package(models.Model):
    vendor = models.ForeignKey(Vendor)
    name = models.CharField(max_length=200, blank=True, null=True)
    purchasing_options = models.ManyToManyField(PurchasingOptions, related_name='purchasing_options')
    commercial_purchasing_options = models.ManyToManyField(PurchasingOptions, related_name='commercial_purchasing_options', blank=True, null=True)
    insurance = models.CharField(max_length=200, blank=True, null=True)
    monitoring_and_maintenance = models.CharField(max_length=200, blank=True, null=True)
    credit_requirements = models.CharField(max_length=200, blank=True, null=True)
    lien_specifics = models.CharField(max_length=200, blank=True, null=True)
    cancellation_and_returns = models.CharField(max_length=200, blank=True, null=True)
    relocation = models.CharField(max_length=200, blank=True, null=True)
    shading_issues = models.CharField(max_length=200, blank=True, null=True)
    upgrades = models.CharField(max_length=200, blank=True, null=True)
    net_energy_metering = models.CharField(max_length=200, blank=True, null=True)
    panel_efficiency = models.CharField(max_length=200, blank=True, null=True)
    panel_country_of_origin = models.CharField(max_length=200, blank=True, null=True)
    inverter_microinverter = models.CharField(max_length=200, blank=True, null=True)
    energy_storage = models.CharField(max_length=200, blank=True, null=True)
    suitable_roof_types = models.CharField(max_length=200, blank=True, null=True)
    installation = models.CharField(max_length=200, blank=True, null=True)
    installation_time = models.CharField(max_length=200, blank=True, null=True)
    general_info = models.CharField(max_length=200, blank=True, null=True)
    electric_vehicle_charging = models.CharField(max_length=200, blank=True, null=True)
    permitting = models.CharField(max_length=200, blank=True, null=True)
    additional_services = models.CharField(max_length=200, blank=True, null=True)
    referral_program = models.CharField(max_length=200, blank=True, null=True)
    multiple_property_discounts = models.CharField(max_length=200, blank=True, null=True)
    price_per_kwh = models.CharField(max_length=200, blank=True, null=True)
    turn_around_time = models.CharField(max_length=200, blank=True, null=True)
    ground_mounts = models.CharField(max_length=200, blank=True, null=True)
    impressions = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)
    phone_clicks = models.IntegerField(default=0)
    website_clicks = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
        unique_together = (("vendor", "name"),)

    def __str__(self):
        return '{}: {}'.format(self.vendor.name, self.id)


@python_2_unicode_compatible
class Proposal(models.Model):
    loi = models.ForeignKey(LOI)
    package = models.ForeignKey(Package)
    status = models.ForeignKey(StatusOptions, blank=True, null=True)
    documents = models.CharField(max_length=500, blank=True, null=True)
    real_estate_agent = models.ForeignKey(RealEstateAgent, blank=True, null=True)
    energy_advisor = models.ForeignKey(EnergyAdvisor, blank=True, null=True)

    class Meta:
        verbose_name = 'Proposal'
        verbose_name_plural = 'Proposals'

    def __str__(self):
        return '{}: ({}) {}'.format(self.loi.enduser.name, self.package.vendor.name, self.package.name)


@python_2_unicode_compatible
class OtpCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField('OTP Code', blank=True, null=True)
    is_activated = models.BooleanField('Is Activated', default=False)
    activated_on = models.DateTimeField('Activated on', blank=True)

    class Meta:
        verbose_name = 'Opt Code'
        verbose_name_plural = 'Opt Codes'

    def __str__(self):
        return 'User id-{}, Code-{}'.format(self.user, self.code)


@python_2_unicode_compatible
class OtpCodesGenerated(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField('OTP Code', blank=True, null=True)

    class Meta:
        verbose_name = 'Generated Opt Code'
        verbose_name_plural = 'Generated Opt Codes'

    def __str__(self):
        return 'User id-{}, Code-{}'.format(self.user, self.code)