from django.conf.urls import url
from ajax_select import urls as ajax_select_urls
from . import views


try:
    from django.conf.urls import patterns, url, include
except:
    from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.new_exp,{}, name='new'),
	url(r'^edit/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.new_exp,{}, name='edit'),
	url(r'^export/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.export_csv,{}, name='export'),
	url(r'^import/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.import_csv,{}, name='import'),
	url(r'^delete/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.new_exp,{}, name='delete'),
	url(r'^new/confirm/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.new_confirm, name='new_confirm'),
	url(r'^new/example', views.new_exp_example, name='new_example'),
	url(r'^get/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',views.detail, name='detail'),
	#url(r'^search/$', views.OrderListJson.as_view(), name='order_list_json'),
#	url(r'^search/$', views.Experiment_asJson, name='my_ajax_url'),
#	url(r'^search2/$', views.OrderListJson.as_view(), name='order_list_json'),
	url(r'^search/$', views.datatable, name='datatable'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^login/$', views.login, name='login'),
	url(r'^console/$', views.console, name='console'),

	url(r'/physical/', views.physical_search, name='physical_search')
]
