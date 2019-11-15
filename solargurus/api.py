from tastypie.resources import ModelResource, ALL
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication, SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields, utils
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from solargurus.models import EndUser, Vendor, PurchasingOptions, LOI, Package, Proposal, StatusOptions, EnergyAdvisor, RealEstateAgent

class EndUserResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = EndUser.objects.all()
        resource_name = 'enduser'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'email': ALL_WITH_RELATIONS,
            'password': ALL_WITH_RELATIONS,
            'id': ALL_WITH_RELATIONS,
        }


class RealEstateAgentResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = RealEstateAgent.objects.all()
        resource_name = 'realestateagent'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'email': ALL_WITH_RELATIONS,
            'password': ALL_WITH_RELATIONS
        }


class VendorResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Vendor.objects.all()
        resource_name = 'vendor'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'id': ALL_WITH_RELATIONS,
            'zipcode': ALL_WITH_RELATIONS,
            'email': ALL_WITH_RELATIONS,
            'password': ALL_WITH_RELATIONS
        }


class EnergyAdvisorResource(ModelResource):
    vendor = fields.ForeignKey(VendorResource, 'vendor', null=True, full=True)
    class Meta:
        always_return_data = True
        queryset = EnergyAdvisor.objects.all()
        resource_name = 'energyadvisor'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'email': ALL_WITH_RELATIONS,
            'password': ALL_WITH_RELATIONS,
            'vendor': ALL_WITH_RELATIONS
        }

class StatusOptionsResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = StatusOptions.objects.all()
        resource_name = 'statusoptions'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'id': ALL_WITH_RELATIONS,
            'name': ALL_WITH_RELATIONS,

        }


class PurchasingOptionsResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = PurchasingOptions.objects.all()
        resource_name = 'purchasingoptions'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0

class LOIResource(ModelResource):
    enduser = fields.ForeignKey(EndUserResource, 'enduser', null=True, full=True)
    class Meta:
        always_return_data = True
        queryset = LOI.objects.all()
        resource_name = 'loi'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'referral_code': ALL_WITH_RELATIONS,
            'enduser': ALL_WITH_RELATIONS,
        }

class PackageResource(ModelResource):
    vendor = fields.ForeignKey(VendorResource, 'vendor', null=True, full=True)
    purchasing_options = fields.ManyToManyField(PurchasingOptionsResource, 'purchasing_options', null=True, full=True)
    class Meta:
        always_return_data = True
        queryset = Package.objects.all()
        resource_name = 'package'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'zipcode': ALL_WITH_RELATIONS,
            'vendor': ALL_WITH_RELATIONS,
        }

class ProposalResource(ModelResource):

    loi = fields.ForeignKey(LOIResource, 'loi', null=True, full=True)
    package = fields.ForeignKey(PackageResource, 'package', null=True, full=True)
    status = fields.ForeignKey(StatusOptionsResource, 'status', null=True, full=True)
    energy_advisor = fields.ForeignKey(EnergyAdvisorResource, 'energy_advisor', null=True, full=True)
    real_estate_agent = fields.ForeignKey(RealEstateAgentResource, 'real_estate_agent', null=True, full=True)
    class Meta:
        always_return_data = True
        queryset = Proposal.objects.all()
        resource_name = 'proposal'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
        limit = 0
        filtering = {
            'loi': ALL_WITH_RELATIONS,
            'package': ALL_WITH_RELATIONS,
            'status': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        print 'running dehydrate'
        referral_code = bundle.data.get('loi').data.get('referral_code')

        if referral_code != "" and not None:
            energyadvisor = EnergyAdvisor.objects.filter(referral_code=referral_code)
            realestateagent = RealEstateAgent.objects.filter(referral_code=referral_code)
            if bundle.data.get('energy_advisor') is None:
                if len(energyadvisor):
                    bundle.data['energy_advisor'] = '/api/energyadvisor/' + str(energyadvisor[0].id) + '/'
            if bundle.data.get('real_estate_agent') is None:
                if len(realestateagent):
                    bundle.data['real_estate_agent'] = '/api/realestateagent/' + str(realestateagent[0].id) + '/'
        self.obj_create(bundle)
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        print 'running obj_create'
        bundle = super(ProposalResource, self).obj_create(
            bundle)


        return bundle
