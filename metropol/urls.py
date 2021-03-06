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
from metropol_abogados.forms import ValidatingPasswordChangeForm


urlpatterns = [
    # Translation URLS
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Auth URLS
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name="logout"),
    url(r'^password_change/$', auth_views.password_change, {'password_change_form': ValidatingPasswordChangeForm, 'template_name': 'user/password_change.html', 'post_change_redirect': '/'}, name='password-change'),
    # Welcome URL
    url(r'^$', 'metropol_abogados.views.StaticViews.index', name="index"),
    # Application views
    url(r'^metropol/', include('metropol_abogados.urls')),
]
