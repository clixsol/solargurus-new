from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^enter_zipcode/', views.enter_zipcode, name='enter_zipcode'),
    url(r'^phoneclick/', views.phoneclick, name='phoneclick'),
    url(r'^websiteclick/', views.websiteclick, name='websiteclick'),
    url(r'^view_package/(?P<pid>\d+)/$', views.view_package, name='view_package'),
    url(r'^get_offer/(?P<pid>\d+)/$', views.get_offer, name='get_offer'),
    url(r'^usage_info/(?P<pid>\d+)/$', views.usage_info, name='usage_info'),
    url(r'^complete/(?P<pid>\d+)/$', views.complete, name='complete'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^sign_up/$', views.MySignUpView.as_view(), name='sign_up'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset_done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^auth_password_reset_confirm/$', auth_views.auth_password_reset_confirm, name='auth_password_reset_confirm'),
    # url(r'^registration_register/$', auth_views.registration_register, name='registration_register'),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    # url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url='/solargurus/')),
    # url(r'^password-reset/<uidb64>/<token>/', empty_view, name='password_reset_confirm'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    # url(r'^opt-code/(?P<user_id>\d+)/$', views.opt_code_generation, name='opt_code_generation')
]
