"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from solargurus.api import EndUserResource, VendorResource, PurchasingOptionsResource, LOIResource, PackageResource, ProposalResource, StatusOptionsResource, EnergyAdvisorResource, RealEstateAgentResource

from solargurus import views

enduser_resource = EndUserResource()
vendor_resource = VendorResource()
purchasingoptions_resource = PurchasingOptionsResource()
loi_resource = LOIResource()
package_resource = PackageResource()
proposal_resource = ProposalResource()
statusoptions_resource = StatusOptionsResource()
energyadvisor_resource = EnergyAdvisorResource()
realestateagent_resource = RealEstateAgentResource()

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(enduser_resource.urls)),
    url(r'^api/', include(vendor_resource.urls)),
    url(r'^api/', include(purchasingoptions_resource.urls)),
    url(r'^api/', include(loi_resource.urls)),
    url(r'^api/', include(package_resource.urls)),
    url(r'^api/', include(proposal_resource.urls)),
    url(r'^api/', include(statusoptions_resource.urls)),
    url(r'^api/', include(energyadvisor_resource.urls)),
    url(r'^api/', include(realestateagent_resource.urls)),
    url(r'^s3/signature', views.handle_s3, name="s3_signee"),
    url(r'^s3/delete', views.handle_s3, name='s3_delete'),
    url(r'^s3/success', views.success_redirect_endpoint, name="s3_succes_endpoint"),
    url(r'^solargurus/', include('solargurus.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url('^', include('django.contrib.auth.urls'))
]
