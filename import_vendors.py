import os
import csv
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'
application = get_wsgi_application()

from solargurus.models import Vendor, Package, PurchasingOptions

with open('csv/vendors.csv', 'rb') as f:
    reader = csv.reader(f)
    headers = []
    vendors = []

    for i, row in enumerate(reader):
        if i == 0:
            headers = row
        else:
            vendor = {}

            for x, value in enumerate(row):
                header = headers[x]
                vendor[header] = value
            vendors.append(vendor)


for i, vendor in enumerate(vendors):

    v = Vendor.objects.update_or_create(name=vendor['name'], defaults=vendor)[0]

    Vendor.save(v)
    po = PurchasingOptions.objects.all()
    package = {
        'vendor': v,
        'name': "{}'s Solar Package".format(vendor['name']),
        'purchasing_options': po,
        'commercial_purchasing_options': po,
        'insurance': 'We work with all forms of homeowner\'s insurance',
        'monitoring_and_maintenance': 'We monitor... and perform maintenance.',
        'credit_requirements': 'Must have a FICO score above 650',
        'lien_specifics': 'Don\'t lien too far... or you\'ll fall over',
        'cancellation_and_returns': 'No cancellations or returns.',
        'relocation': 'Purchase includes 1 free relocation of services.',
        'shading_issues': 'No shading issues.',
        'upgrades': 'No upgrades... this is all you\'ll ever need.',
        'net_energy_metering': 'Sure.',
        'panel_efficiency': 'Super-duper efficient.',
        'panel_country_of_origin': 'Malaysia',
        'inverter_microinverter': 'Comes with both inverter and micro inverter.',
        'energy_storage': 'Additional energy storage is sold separately.',
        'suitable_roof_types': 'All roofs are suitable.',
        'installation': 'Installation takes about 3 hours and is included in the price.',
        'referral_program': 'We\'ll pay you $100 for every person you refer that signs up with our service.',
        'multiple_property_discounts': 'On a case by case basis.'
    }
    p = Package.objects.create(
        vendor=package['vendor'],
        name=package['name'],

        insurance=package['insurance'],
        monitoring_and_maintenance=package['monitoring_and_maintenance'],
        credit_requirements=package['credit_requirements'],
        lien_specifics=package['lien_specifics'],
        cancellation_and_returns=package['cancellation_and_returns'],
        relocation=package['relocation'],
        shading_issues=package['shading_issues'],
        upgrades=package['upgrades'],
        net_energy_metering=package['net_energy_metering'],
        panel_country_of_origin=package['panel_country_of_origin'],
        panel_efficiency=package['panel_efficiency'],
        inverter_microinverter=package['inverter_microinverter'],
        energy_storage=package['energy_storage'],
        suitable_roof_types=package['suitable_roof_types'],
        installation=package['installation'],
        referral_program=package['referral_program'],
        multiple_property_discounts=package['multiple_property_discounts']
    )
    Package.save(p)
    p.purchasing_options = po
    p.commercial_purchasing_options = po

    Package.save(p)
