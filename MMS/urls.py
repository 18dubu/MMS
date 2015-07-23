"""MMS URL Configuration

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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = [
	url(r'^$',include('virtual_miseq.urls')),
	url(r'^virtual/',include('virtual_miseq.urls')),
	url(r'^physical/',include('virtual_miseq.urls')),
        url(r'^admin/', include(admin.site.urls)),
#	url(r'^admin/lookups/', include(ajax_select_urls)),
	url(r'^lookups/', include(ajax_select_urls)),
#	url(r'^search/',include('virtual_miseq.urls')),
	#url(r'lookups/', include(ajax_select_urls)),
	url(r'^selectable/', include('selectable.urls')),
	url(r'^contact/', include('envelope.urls')),
]