from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from .views import PersonViews, AddressViews, PhoneViews, ExpedientViews, PhaseViews

urlpatterns = [
    # REST API urls
    url(r'^api/phase/list/$', PhaseViews.phase_by_branch_json, name="api-phase-list"),
    # Person views
    url(r'^person/list/$', PersonViews.person_list, name='person-list'),
    url(r'^person/details/(?P<pk>\d+)/$', permission_required('auth.management_metropol')(PersonViews.DetailsView.as_view()), name='person-details'),
    url(r'^person/create/$', PersonViews.edit, name="person-create"),
    url(r'^person/edit/(?P<person_id>\d+)/$', PersonViews.edit, name="person-edit"),
    url(r'^person/delete/(?P<person_id>\d+)/$', PersonViews.delete, name="person-delete"),
    # Phone views
    url(r'^phone/create/(?P<person_id>\d+)/$', PhoneViews.edit, name="phone-create"),
    url(r'^phone/edit/(?P<person_id>\d+)/(?P<phone_id>\d+)/$', PhoneViews.edit, name="phone-edit"),
    url(r'^phone/delete/(?P<phone_id>\d+)/$', PhoneViews.delete, name="phone-delete"),
    # Address views
    url(r'^address/create/(?P<person_id>\d+)/$', AddressViews.edit, name="address-create"),
    url(r'^address/edit/(?P<person_id>\d+)/(?P<address_id>\d+)/$', AddressViews.edit, name="address-edit"),
    url(r'^address/delete/(?P<address_id>\d+)/$', AddressViews.delete, name="address-delete"),
    # Expedient views
    url(r'^expedient/list/$', ExpedientViews.expedient_list, name="expedient-list"),
    url(r'^expedient/details/(?P<pk>\d+)/$', permission_required('auth.management_metropol')(ExpedientViews.DetailsView.as_view()), name='expedient-details'),
    url(r'^expedient/create/$', ExpedientViews.edit, name="expedient-create"),
    url(r'^expedient/edit/(?P<expedient_id>\d+)/$', ExpedientViews.edit, name="expedient-edit"),
    url(r'^expedient/delete/(?P<expedient_id>\d+)/$', ExpedientViews.delete, name="expedient-delete"),
]