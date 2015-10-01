"""metropol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Translation URLS
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Application views
    url(r'^$', 'metropol_abogados.views.StaticViews.index', name="login"),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name="logout"),
    # Person views
    url(r'^manager/person/list/$', 'metropol_abogados.views.PersonViews.person_list', name='person-list'),
    url(r'^manager/person/details/(?P<person_id>\d+)/$', 'metropol_abogados.views.PersonViews.details', name='person-details'),
    url(r'^manager/person/create/$', 'metropol_abogados.views.PersonViews.edit', name="person-create"),
    url(r'^manager/person/edit/(?P<person_id>\d+)/$', 'metropol_abogados.views.PersonViews.edit', name="person-edit"),
    url(r'^manager/person/delete/(?P<person_id>\d+)/$', 'metropol_abogados.views.PersonViews.delete', name="person-delete"),
    # Phone views
    url(r'^manager/phone/create/(?P<person_id>\d+)/$', 'metropol_abogados.views.PhoneViews.edit', name="phone-create"),
    url(r'^manager/phone/edit/(?P<person_id>\d+)/(?P<phone_id>\d+)/$', 'metropol_abogados.views.PhoneViews.edit', name="phone-edit"),
    url(r'^manager/phone/delete/(?P<phone_id>\d+)/$', 'metropol_abogados.views.PhoneViews.delete', name="phone-delete"),
]
