from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from solargurus.forms import EnterZipCode, GetOffer, UsageInfo, VendorProfile, EnergyAdvisorProfile, RealEstateAgentProfile
from solargurus.models import Vendor, Package, EndUser, LOI, PurchasingOptions, Proposal, Area, Account, RealEstateAgent, EnergyAdvisor, LeadTypes
from solargurus.models import OtpCodesGenerated, OtpCode
from solargurus.twillio import Notifciation
from datetime import datetime

from otp_code import generateOTP
from django.views import View
import json
from django.core import serializers
from django.forms.models import model_to_dict
from itertools import chain
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests

import base64, hmac, hashlib, json, sys


try:
    import boto
    from boto.s3.connection import Key, S3Connection
    boto.set_stream_logger('boto')
    # S3 = S3Connection(settings.AWS_SERVER_PUBLIC_KEY, settings.AWS_SERVER_SECRET_KEY)
except ImportError, e:
    print("Could not import boto, the Amazon SDK for Python.")
    print("Deleting files will not work.")
    print("Install boto with")
    print("$ pip install boto")


@csrf_exempt
def phoneclick(request):
    if request.method == "POST":
        package_id = request.POST.get('package_id', None)
        if package_id is not None:
            package = Package.objects.get(id=package_id)
            package.phone_clicks += 1
            Package.save(package)
    return make_response(200)


@csrf_exempt
def websiteclick(request):
    if request.method == "POST":
        package_id = request.POST.get('package_id', None)
        if package_id is not None:
            package = Package.objects.get(id=package_id)
            package.website_clicks += 1
            Package.save(package)
    return make_response(200)

@csrf_exempt
def success_redirect_endpoint(request):
    """ This is where the upload will snd a POST request after the
    file has been stored in S3.
    """
    return make_response(200)

@csrf_exempt
def handle_s3(request):
    """ View which handles all POST and DELETE requests sent by Fine Uploader
    S3. You will need to adjust these paths/conditions based on your setup.
    """
    if request.method == "POST":
        return handle_POST(request)
    elif request.method == "DELETE":
        return handle_DELETE(request)
    else:
        return HttpResponse(status=405)

def handle_POST(request):
    """ Handle S3 uploader POST requests here. For files <=5MiB this is a simple
    request to sign the policy document. For files >5MiB this is a request
    to sign the headers to start a multipart encoded request.
    """
    if request.POST.get('success', None):
        return make_response(200)
    else:
        request_payload = json.loads(request.body)
        headers = request_payload.get('headers', None)
        if headers:
            # The presence of the 'headers' property in the request payload
            # means this is a request to sign a REST/multipart request
            # and NOT a policy document
            response_data = sign_headers(headers)
        else:
            print('request_payload:')
            print(request_payload)
            if not is_valid_policy(request_payload):
                print('not valid policy')
                return make_response(400, {'invalid': True})
            response_data = sign_policy_document(request_payload)
        response_payload = json.dumps(response_data)
        return make_response(200, response_payload)

def handle_DELETE(request):
    """ Handle file deletion requests. For this, we use the Amazon Python SDK,
    boto.
    """
    if boto:
        bucket_name = request.REQUEST.get('bucket')
        key_name = request.REQUEST.get('key')
        aws_bucket = S3.get_bucket(bucket_name, validate=False)
        aws_key = Key(aws_bucket, key_name)
        aws_key.delete()
        return make_response(200)
    else:
        return make_response(500)

def make_response(status=200, content=None):
    """ Construct an HTTP response. Fine Uploader expects 'application/json'.
    """
    response = HttpResponse()
    response.status_code = status
    response['Content-Type'] = "application/json"
    response.content = content
    return response

def is_valid_policy(policy_document):
    """ Verify the policy document has not been tampered with client-side
    before sending it off.
    """
    #bucket = settings.AWS_EXPECTED_BUCKET
    #parsed_max_size = settings.AWS_MAX_SIZE
    bucket = ''
    parsed_max_size = 0

    for condition in policy_document['conditions']:
        if isinstance(condition, list) and condition[0] == 'content-length-range':
            parsed_max_size = condition[2]
        else:
            if condition.get('bucket', None):
                bucket = condition['bucket']
    print(bucket)
    print(parsed_max_size)
    print(settings.AWS_EXPECTED_BUCKET)
    print(settings.AWS_MAX_SIZE)
    return bucket == settings.AWS_EXPECTED_BUCKET and parsed_max_size == settings.AWS_MAX_SIZE

def sign_policy_document(policy_document):
    """ Sign and return the policy doucument for a simple upload.
    http://aws.amazon.com/articles/1434/#signyours3postform
    """
    policy = base64.b64encode(json.dumps(policy_document))
    signature = base64.b64encode(hmac.new(settings.AWS_CLIENT_SECRET_KEY, policy, hashlib.sha1).digest())
    return {
        'policy': policy,
        'signature': signature
    }

def sign_headers(headers):
    """ Sign and return the headers for a chunked upload. """
    return {
        'signature': base64.b64encode(hmac.new(settings.AWS_CLIENT_SECRET_KEY, headers, hashlib.sha1).digest())
    }


def db_instance2dict(instance):
    from django.db.models.fields.related import ManyToManyField
    metas = instance._meta
    data = {}
    for f in chain(metas.concrete_fields, metas.many_to_many):
        if isinstance(f, ManyToManyField):
            data[str(f.name)] = {tmp_object.pk: db_instance2dict(tmp_object)
                                 for tmp_object in f.value_from_object(instance)}
        else:
            data[str(f.name)] = str(getattr(instance, f.name, False))
    return data


class MySignUpView(View):
    form_class = UserCreationForm
    template_name = 'registration/sign_up.html'
    def get(self, request, *args, **kwargs):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                # <process form cleaned data>
                u = User.objects.create_user(
                        form.cleaned_data.get('username'),
                        '',# request.POST['email'],
                        form.cleaned_data.get('password1'),
                        is_active = True
                )
                print(request.POST.get('account_type'))
                account = Account(
                    user=u,
                    type=request.POST.get('account_type')
                )
                account.save()
                # TODO Display message and redirect to login
                return HttpResponseRedirect('/solargurus/login/?next=/solargurus/profile')
            return render(request, self.template_name, {'form': form})


def view_package(request, pid):
    pid = int(pid)
    # vendor = Vendor.objects.get(id=pid)
    # print vendor
    package = Package.objects.get(id=pid)
    package.page_views += 1
    Package.save(package)
    print package.page_views
    associations = []
    if package.vendor.associations:
        associations = package.vendor.associations.split(',')
    context = {
        'package': package,
        'associations': associations
    }
    return render(request, "solargurus/package.html", context)


def profile(request):
    twillio_notification = Notifciation()
    message = """
               Thank you for joining the Solar Gurus family and making our planet a cleaner and healthier place to live!

               This is your unique code:
               {}
               """
    print('authenticated:')
    print(request.user.is_authenticated)
    print(request.user.account.type)
    if request.user.is_authenticated:
        if request.user.account.type == 'RealEstateAgent':
            context = {
                'real_estate_agent': json.dumps(None),
                'ra': None,
                'num_referrals': 0
            }
            if request.method == 'POST':
                form = RealEstateAgentProfile(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    address = form.cleaned_data['address']
                    city = form.cleaned_data['city']
                    state = form.cleaned_data['state']
                    zipcode = form.cleaned_data['zipcode']
                    website = form.cleaned_data['website']
                    logo = form.cleaned_data['logo']
                    code = generateOTP()
                    OtpCodesGenerated.objects.create(
                        user_id=request.user.id,
                        code=code,
                    )
                    twillio_notification.send_messsage(
                        message.format(str(code)), phone)

                    real_estate_agent, created = RealEstateAgent.objects.update_or_create(
                        user=request.user,
                        name=name,
                        email=email,
                        address=address,
                        city=city,
                        state=state,
                        zipcode=zipcode,
                        phone=phone,
                        website=website,
                        logo=logo
                    )
                else:
                    print('not valid')
                    print(form.errors)
            real_estate_agents = RealEstateAgent.objects.filter(user=request.user)
            if len(real_estate_agents):
                real_estate_agent = real_estate_agents.all()[0]
                context['ra'] = real_estate_agent
                context['real_estate_agent'] = json.dumps(model_to_dict(real_estate_agent))
                num_referrals = len(LOI.objects.filter(referral_code=real_estate_agent.referral_code))
                context['num_referrals'] = num_referrals
            return render(request, "solargurus/realestateagent_profile.html", context)
        if request.user.account.type == 'EnergyAdvisor':
            print('WE ARE EnergyAdvisor')
            context = {
                'energy_advisor': json.dumps(None),
                'ea': None,
                'num_referrals': 0
            }
            if request.method == 'POST':
                form = EnergyAdvisorProfile(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    address = form.cleaned_data['address']
                    city = form.cleaned_data['city']
                    state = form.cleaned_data['state']
                    zipcode = form.cleaned_data['zipcode']
                    website = form.cleaned_data['website']
                    logo = form.cleaned_data['logo']
                    code = generateOTP()
                    OtpCodesGenerated.objects.create(
                        user_id=request.user.id,
                        code=code,
                    )
                    twillio_notification.send_messsage(
                        message.format(str(code)), phone)
                    print("logo:")
                    print(logo)
                    energy_advisor, created = EnergyAdvisor.objects.update_or_create(
                        user=request.user,
                        name=name,
                        email=email,
                        address=address,
                        city=city,
                        state=state,
                        zipcode=zipcode,
                        phone=phone,
                        website=website,
                        logo=logo
                    )
                else:
                    print('not valid')
                    print(form.errors)
            energy_advisors = EnergyAdvisor.objects.filter(user=request.user)
            if len(energy_advisors):
                energy_advisor = energy_advisors.all()[0]
                context['ea'] = energy_advisor
                context['energy_advisor'] = json.dumps(model_to_dict(energy_advisor))
                num_referrals = len(LOI.objects.filter(referral_code=energy_advisor.referral_code))
                context['num_referrals'] = num_referrals
                print(context['ea'])
            print(context)
            return render(request, "solargurus/energyadvisor_profile.html", context)
        if request.user.account.type == 'Vendor':
            context = {
                'vendor': json.dumps(None),
                'package': json.dumps(None),
                'stats': {
                    'lois': 0,
                    'proposals_sent': 0,
                    'proposals_accepted': 0,
                    'proposals_phone': 0,
                    'proposals_email': 0,
                    'proposals_website': 0,
                    'impressions': 0,
                    'page_views': 0,
                    'phone_clicks': 0,
                    'website_clicks': 0
                }
            }
            if request.method == 'POST':
                form = VendorProfile(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    address = form.cleaned_data['address']
                    city = form.cleaned_data['city']
                    state = form.cleaned_data['state']
                    zipcode = form.cleaned_data['zipcode']
                    website = form.cleaned_data['website']
                    logo = form.cleaned_data['logo']
                    banner = form.cleaned_data['banner']
                    slogan = form.cleaned_data['slogan']
                    accolades = form.cleaned_data['accolades']
                    associations = form.cleaned_data['associations']
                    package_name = form.cleaned_data['package_name']
                    purchasing_options = form.cleaned_data['purchasing_options']
                    commercial_purchasing_options = form.cleaned_data['commercial_purchasing_options']
                    insurance = form.cleaned_data['insurance']
                    monitoring_and_maintenance = form.cleaned_data['monitoring_and_maintenance']
                    credit_requirements = form.cleaned_data['credit_requirements']
                    lien_specifics = form.cleaned_data['lien_specifics']
                    cancellation_and_returns = form.cleaned_data['cancellation_and_returns']
                    relocation = form.cleaned_data['relocation']
                    shading_issues = form.cleaned_data['shading_issues']
                    upgrades = form.cleaned_data['upgrades']
                    net_energy_metering = form.cleaned_data['net_energy_metering']
                    panel_efficiency = form.cleaned_data['panel_efficiency']
                    panel_country_of_origin = form.cleaned_data['panel_country_of_origin']
                    inverter_microinverter = form.cleaned_data['inverter_microinverter']
                    energy_storage = form.cleaned_data['energy_storage']
                    suitable_roof_types = form.cleaned_data['suitable_roof_types']
                    installation = form.cleaned_data['installation']
                    installation_time = form.cleaned_data['installation_time']
                    general_info = form.cleaned_data['general_info']
                    electric_vehicle_charging = form.cleaned_data['electric_vehicle_charging']
                    permitting = form.cleaned_data['permitting']
                    additional_services = form.cleaned_data['additional_services']
                    referral_program = form.cleaned_data['referral_program']
                    multiple_property_discounts = form.cleaned_data['multiple_property_discounts']
                    price_per_kwh = form.cleaned_data['price_per_kwh']
                    turn_around_time = form.cleaned_data['turn_around_time']
                    ground_mounts = form.cleaned_data['ground_mounts']
                    print(turn_around_time)
                    print(logo)
                    print(banner)
                    code = generateOTP()
                    OtpCodesGenerated.objects.create(
                        user_id=request.user.id,
                        code=code,
                    )
                    twillio_notification.send_messsage(
                        message.format(str(code)), phone)
                    vendor, created = Vendor.objects.update_or_create(
                        user=request.user,
                        name=name,
                        email=email,
                        address=address,
                        city=city,
                        state=state,
                        zipcode=zipcode,
                        phone=phone,
                        website=website,
                        img=banner,
                        logo=logo,
                        slogan=slogan,
                        accolades=accolades,
                        associations=associations.strip()
                    )
                    print(created)
                    print(vendor)
                    # vendor.save()
                    package, created = Package.objects.update_or_create(
                        vendor=vendor,
                        name=vendor.name,
                        # purchasing_options=[int(p) for p in purchasing_options],
                        # commercial_purchasing_options=[int(c) for c in commercial_purchasing_options],
                        insurance=insurance,
                        monitoring_and_maintenance=monitoring_and_maintenance,
                        credit_requirements=credit_requirements,
                        lien_specifics=lien_specifics,
                        cancellation_and_returns=cancellation_and_returns,
                        relocation=relocation,
                        shading_issues=shading_issues,
                        upgrades=upgrades,
                        net_energy_metering=net_energy_metering,
                        panel_efficiency=panel_efficiency,
                        panel_country_of_origin=panel_country_of_origin,
                        inverter_microinverter=inverter_microinverter,
                        energy_storage=energy_storage,
                        suitable_roof_types=suitable_roof_types,
                        installation=installation,
                        installation_time=installation_time,
                        general_info=general_info,
                        electric_vehicle_charging=electric_vehicle_charging,
                        permitting=permitting,
                        additional_services=additional_services,
                        referral_program=referral_program,
                        multiple_property_discounts=multiple_property_discounts,
                        price_per_kwh=price_per_kwh,
                        turn_around_time=turn_around_time,
                        ground_mounts=ground_mounts
                    )
                    for purchasing_option in purchasing_options:
                        package.purchasing_options.add(PurchasingOptions.objects.get(name=purchasing_option))
                    for purchasing_option in commercial_purchasing_options:
                        package.commercial_purchasing_options.add(PurchasingOptions.objects.get(name=purchasing_option))
                    package.save()
                    print(purchasing_options)
                else:
                    print('not valid')
                    print(form.errors)

            vendors = Vendor.objects.filter(user=request.user)
            if len(vendors):
                vendor = vendors.all()[0]

                context['vendor'] = json.dumps(model_to_dict(vendor))
                packages = Package.objects.filter(vendor=vendor)
                print(len(packages))
                if len(packages):
                    package = packages.all()[0]
                    print('package:')
                    print(package.page_views)
                    context['package'] = json.dumps(db_instance2dict(package))
                    proposals = Proposal.objects.filter(package=package)
                    proposals_sent = proposals.filter(status__name="Sent")
                    proposals_accepted = proposals.filter(status__name="Accepted")
                    proposals_phone = proposals.filter(loi__lead_source__name="Phone")
                    proposals_email = proposals.filter(loi__lead_source__name="Email")
                    proposals_website = proposals.filter(loi__lead_source__name="Website")

                    print('proposals:')
                    print(proposals)
                    context['stats'] = {
                        'lois': len(proposals),
                        'proposals_sent': len(proposals_sent),
                        'proposals_accepted': len(proposals_accepted),
                        'proposals_phone': len(proposals_phone),
                        'proposals_email': len(proposals_email),
                        'proposals_website': len(proposals_website),
                        'impressions': package.impressions,
                        'page_views': package.page_views,
                        'phone_clicks': package.phone_clicks,
                        'website_clicks': package.website_clicks
                    }
                    # package.purchasing_options = model_to_dict(package.purchasing_options)
                    # context['package'] = json.dumps(model_to_dict(package))
            return render(request, "solargurus/vendor_profile.html", context)


    return HttpResponseRedirect('/solargurus/login/?next=/solargurus/profile')


def enter_zipcode(request):
    zipcode = request.GET.get('zipcode', None)
    num_results = 0
    packages = []
    background_img = '/static/img/sub_header_short.jpg'

    if request.method == 'POST':
        form = EnterZipCode(request.POST)
        if form.is_valid():
            zipcode = form.cleaned_data['zipcode']
    print zipcode
    packages = Package.objects.filter(vendor__zipcode=zipcode)
    for package in packages:
        package.impressions += 1
        Package.save(package)
    area = Area.objects.filter(zipcodes__contains=[str(zipcode)])
    print area
    if len(area):
        background_img = area[0].img
    print packages
    num_results = len(packages)
    context = {
        'zipcode': zipcode,
        'num_results': num_results,
        'packages': packages,
        'background_img': background_img


    }
    print(packages)
    return render(request, "solargurus/results.html", context)


def complete(request, pid):
    if request.method == 'POST':
        print "whoo we posted"
        form = UsageInfo(request.POST)
        print form
        if form.is_valid():
            print "whoo valid"
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            roof_material = form.cleaned_date['roof_material']
            utility_provider = form.cleaned_data['utility_provider']
            account_number = form.cleaned_data['account_number']
            meter_number = form.cleaned_data['meter_number']
            payment_options = form.cleaned_data['payment_options']
            print "payment options:"
            print payment_options
            payment_methods = PurchasingOptions.objects.filter(id__in=[int(id) for id in payment_options])
            comments = form.cleaned_data['comments']
            referral_code = form.cleaned_data['referral_code']
            enduser_id = request.session['enduser']
            enduser = EndUser.objects.get(id=enduser_id)
            web_lead_source = LeadTypes.objects.get(name='Website')
            loi = LOI(
                lead_source=web_lead_source,
                enduser=enduser,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                roof_material=roof_material,
                utility_provider=utility_provider,
                account_number=account_number,
                meter_number=meter_number,
                comments=comments,
                referral_code=referral_code
                )

            LOI.save(loi)
            for payment_method in payment_methods:
                loi.payment_methods.add(payment_method)
            LOI.save(loi)
            package = Package.objects.get(id=pid)
            proposal = Proposal(loi=loi, package=package)
            Proposal.save(proposal)
            context = {
                'package': package
            }
            return render(request, "solargurus/cart_3.html", context)
        else:
            print "not valid"
    package = Package.objects.get(id=pid)
    print package
    context = {
        'package': package
    }
    return render(request, "solargurus/cart_2.html", context)


def usage_info(request, pid):
    if request.method == 'POST':
        print "whoo we posted"
        form = GetOffer(request.POST)
        print form
        if form.is_valid():
            print "whoo valid"
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            roof_material = form.cleaned_data['roof_material']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            utility_provider = form.cleaned_data['utility_provider']
            account_number = form.cleaned_data['account_number']
            meter_number = form.cleaned_data['meter_number']
            payment_options = form.cleaned_data['payment_options']
            user_id = form.cleaned_data['user_id']
            print "payment options:"
            print payment_options
            payment_methods = PurchasingOptions.objects.filter(id__in=[int(id) for id in payment_options])
            comments = form.cleaned_data['comments']
            referral_code = form.cleaned_data['referral_code']
            print name, email, phone
            # end_user = EndUser(name=name, email=email, phone=phone)
            end_user, created = EndUser.objects.update_or_create(
                name=name, email=email, phone=phone
                )
            # EndUser.save(end_user)
            request.session['enduser'] = end_user.id
            enduser_id = request.session['enduser']
            enduser = EndUser.objects.get(id=enduser_id)
            print(enduser)

            # web_lead_source = LeadTypes.objects.get(name='Website')
            post_data = {
                "Full Name": name,
                "Email": email,
                "Phone Number": phone,
                "Full Address": address,
                "City": city,
                "State": state,
                "Zip Code": zipcode,
                "Roof Material": roof_material,
                "Utility Provider": utility_provider,
                "Account Number": account_number,
                "Meter Number": meter_number,
                "Payment Options": payment_options,
                "Comments": comments,
                "Referral Code": referral_code
            }
            r = requests.post('https://hooks.zapier.com/hooks/catch/5996959/o4b56eo/', json=post_data)

            loi = LOI(
                # lead_source=web_lead_source,
                enduser=enduser,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                utility_provider=utility_provider,
                account_number=account_number,
                meter_number=meter_number,
                comments=comments,
                referral_code=referral_code
                )

            LOI.save(loi)
            for payment_method in payment_methods:
                loi.payment_methods.add(payment_method)
            LOI.save(loi)
            package = Package.objects.get(id=pid)
            proposal = Proposal(loi=loi, package=package)
            Proposal.save(proposal)
            package = Package.objects.get(id=pid)
            print package
            context = {
                'package': package,
                'refrel_code': False
            }
            otp = OtpCodesGenerated.objects.filter(user_id=user_id).order_by('-id')[0]
            if otp.code == int(referral_code):
                OtpCode.objects.create(
                    code=otp.code, is_activated=True, user_id=user_id,
                    activated_on=datetime.now()
                )
                return render(request, "solargurus/cart_3.html", context)
            return render(request, "solargurus/cart.html", context)
        else:
            print "not valid"
    package = Package.objects.get(id=pid)
    print package
    context = {
        'package': package
    }
    return render(request, "solargurus/cart.html", context)


def get_offer(request, pid):
    package = Package.objects.get(id=pid)
    print package
    context = {
        'package': package,
        'user_id': request.user.id
    }
    return render(request, "solargurus/cart.html", context)


# def opt_code_generation(request, user_id):
#     message = """
#     Thank you for joining the Solar Gurus family and making our planet a cleaner and healthier place to live!
#
#     This is your unique code:
#     0437
#     """
#     number = '03228009082'
#     genereated_code = OptCodesGenerated.objects.create(
#         user_id=user_id,
#         code=1234,
#     )
#     twillio_notification = Notifciation()
#     twillio_notification.send_messsage(message, number)



def index(request):
    context = {}
    return render(request, "solargurus/index.html", context)
