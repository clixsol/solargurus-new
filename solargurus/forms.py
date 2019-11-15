from django import forms
from .models import PurchasingOptions

class EnterZipCode(forms.Form):

    zipcode = forms.CharField(label='Zipcode', max_length=100)


class GetOffer(forms.Form):
    user_id = forms.IntegerField(label='User id')
    name = forms.CharField(label='Name', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    phone = forms.CharField(label='Phone', max_length=100)
    roof_material = forms.CharField(label='Roof Material', max_length=100)
    choices = [(option.id, option.name) for option in list(PurchasingOptions.objects.all())]
    address = forms.CharField(label='Address', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    zipcode = forms.CharField(label='Zipcode', max_length=100)
    utility_provider = forms.CharField(label='UtilityProvider', max_length=100)
    account_number = forms.CharField(label='AccountNumber', max_length=100)
    meter_number = forms.CharField(label='MeterNumber', max_length=100)
    payment_options = forms.MultipleChoiceField(label='PaymentOptions', widget=forms.CheckboxSelectMultiple, choices=choices, required=False)
    comments = forms.CharField(label='Comments', max_length=500, required=False)
    referral_code = forms.CharField(label='Referral Code', max_length=10, required=False)



class UsageInfo(forms.Form):
    choices = [(option.id, option.name) for option in list(PurchasingOptions.objects.all())]
    address = forms.CharField(label='Address', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    zipcode = forms.CharField(label='Zipcode', max_length=100)
    roof_material = forms.CharField(label='RoofMaterial', max_length=100, required=False)
    utility_provider = forms.CharField(label='UtilityProvider', max_length=100)
    account_number = forms.CharField(label='AccountNumber', max_length=100)
    meter_number = forms.CharField(label='MeterNumber', max_length=100)
    payment_options = forms.MultipleChoiceField(label='PaymentOptions', widget=forms.CheckboxSelectMultiple, choices=choices)
    comments = forms.CharField(label='Comments', max_length=500, required=False)
    referral_code = forms.CharField(label='Referral Code', max_length=10, required=False)


class EnergyAdvisorProfile(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    phone = forms.CharField(label='Phone', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    zipcode = forms.CharField(label='Zipcode', max_length=100)
    website = forms.CharField(label='Website', max_length=100, required=False)
    logo = forms.CharField(label='Logo', max_length=100, required=False)


class RealEstateAgentProfile(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    phone = forms.CharField(label='Phone', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    zipcode = forms.CharField(label='Zipcode', max_length=100)
    website = forms.CharField(label='Website', max_length=100, required=False)
    logo = forms.CharField(label='Logo', max_length=100, required=False)


class VendorProfile(forms.Form):
    choices = [(option.name, option.name) for option in list(PurchasingOptions.objects.all())]
    name = forms.CharField(label='Name', max_length=100, required=False)
    email = forms.CharField(label='Email', max_length=100)
    phone = forms.CharField(label='Phone', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    zipcode = forms.CharField(label='Zipcode', max_length=100)
    website = forms.CharField(label='Website', max_length=100, required=False)
    logo = forms.CharField(label='Logo', max_length=100, required=False)
    banner = forms.CharField(label='Banner', max_length=100, required=False)
    slogan = forms.CharField(label='Slogan', max_length=100, required=False)
    accolades = forms.CharField(label='Accolades', max_length=100, required=False)
    associations = forms.CharField(label='Associations', max_length=1000, required=False)
    package_name = forms.CharField(label='Package Name', max_length=100, required=False)
    purchasing_options = forms.MultipleChoiceField(label='Purchasing Options', widget=forms.CheckboxSelectMultiple, choices=choices, required=False)
    commercial_purchasing_options = forms.MultipleChoiceField(label='Commercial Purchasing Options', widget=forms.CheckboxSelectMultiple, choices=choices, required=False)
    insurance = forms.CharField(label='Insurance', max_length=100, required=False)
    monitoring_and_maintenance = forms.CharField(label='Monitoring & Maintenance', max_length=100, required=False)
    credit_requirements = forms.CharField(label='Credit Requirements', max_length=100, required=False)
    lien_specifics = forms.CharField(label='Lien Specifics', max_length=100, required=False)
    cancellation_and_returns = forms.CharField(label='Cancellation & Returns', max_length=100, required=False)
    relocation = forms.CharField(label='Relocation', max_length=100, required=False)
    shading_issues = forms.CharField(label='Shading Issues', max_length=100, required=False)
    upgrades = forms.CharField(label='Upgrades', max_length=100, required=False)
    net_energy_metering = forms.CharField(label='Net Energy Metering', max_length=100, required=False)
    panel_efficiency = forms.CharField(label='Panel Efficiency', max_length=100, required=False)
    panel_country_of_origin = forms.CharField(label='Panel Country of Origin', max_length=100, required=False)
    inverter_microinverter = forms.CharField(label='Inverter/Microinverter', max_length=100, required=False)
    energy_storage = forms.CharField(label='Energy Storage', max_length=100, required=False)
    suitable_roof_types = forms.CharField(label='Suitable Roof Types', max_length=100, required=False)
    installation = forms.CharField(label='Installation', max_length=100, required=False)
    installation_time = forms.CharField(label='Installation Time', max_length=100, required=False)
    general_info = forms.CharField(label='General Info', max_length=100, required=False)
    electric_vehicle_charging = forms.CharField(label='Electric Vehicle Charging', max_length=100, required=False)
    permitting = forms.CharField(label='Permitting', max_length=100, required=False)
    additional_services = forms.CharField(label='Additional Services', max_length=100, required=False)
    referral_program = forms.CharField(label='Referral Program', max_length=100, required=False)
    multiple_property_discounts = forms.CharField(label='Multiple Property Discounts', max_length=100, required=False)
    price_per_kwh = forms.CharField(label='Price/kWh', max_length=100, required=False)
    turn_around_time = forms.CharField(label='Time Until Installation', max_length=100, required=False)
    ground_mounts = forms.CharField(label='Ground Mounts', max_length=100, required=False)
