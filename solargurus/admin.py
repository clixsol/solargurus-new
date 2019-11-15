from django.contrib import admin

from .models import EndUser, Vendor, PurchasingOptions, LOI, Package, Proposal, EnergyAdvisor, RealEstateAgent, StatusOptions, Area, Account, LeadTypes

admin.site.register(EndUser)
admin.site.register(Vendor)
admin.site.register(PurchasingOptions)
admin.site.register(LOI)
admin.site.register(Package)
admin.site.register(Proposal)
admin.site.register(StatusOptions)
admin.site.register(Area)


class EnergyAdvisorAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'email',
        'address',
        'city',
        'state',
        'zipcode',
        'phone',
        'website',
        'logo',
        'referral_code',
        'password',
        'vendor'
    ]
    readonly_fields=('referral_code',)


admin.site.register(EnergyAdvisor, EnergyAdvisorAdmin)
admin.site.register(LeadTypes)


class RealEstateAgentAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'email',
        'address',
        'city',
        'state',
        'zipcode',
        'phone',
        'website',
        'logo',
        'referral_code',
        'password'
    ]
    readonly_fields=('referral_code',)


admin.site.register(RealEstateAgent, RealEstateAgentAdmin)
admin.site.site_title = 'SolarGurus Administration'
admin.site.site_header = 'SolarGurus Administration'
admin.site.index_title = 'SolarGurus Administration'
admin.site.register(Account)
