from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from .views import PersonViews, AddressViews, PhoneViews, StaticViews
from django.contrib.auth.decorators import permission_required

urlpatterns = patterns('',
    # Application views
    url(r'^$', 'metropol_abogados.views.StaticViews.index', name="login"),
    # Person views
    url(r'^person/list/$', PersonViews.person_list, name='person-list'),
    url(r'^person/details/(?P<pk>\d+)/$', permission_required('auth.management_metropol')(PersonViews.DetailsView.as_view()), name='person-details'),
    url(r'^person/create/$', 'metropol_abogados.views.PersonViews.edit', name="person-create"),
    url(r'^person/edit/(?P<person_id>\d+)/$', 'metropol_abogados.views.PersonViews.edit', name="person-edit"),
    url(r'^person/delete/(?P<person_id>\d+)/$', 'metropol_abogados.views.PersonViews.delete', name="person-delete"),
    # Phone views
    url(r'^phone/create/(?P<person_id>\d+)/$', 'metropol_abogados.views.PhoneViews.edit', name="phone-create"),
    url(r'^phone/edit/(?P<person_id>\d+)/(?P<phone_id>\d+)/$', 'metropol_abogados.views.PhoneViews.edit', name="phone-edit"),
    url(r'^phone/delete/(?P<phone_id>\d+)/$', 'metropol_abogados.views.PhoneViews.delete', name="phone-delete"),
    # Address views
    url(r'^address/create/(?P<person_id>\d+)/$', 'metropol_abogados.views.AddressViews.edit', name="address-create"),
    url(r'^address/edit/(?P<person_id>\d+)/(?P<address_id>\d+)/$', 'metropol_abogados.views.AddressViews.edit', name="address-edit"),
    url(r'^address/delete/(?P<address_id>\d+)/$', 'metropol_abogados.views.AddressViews.delete', name="address-delete"),
)
