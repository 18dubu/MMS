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
	############################Exp#################################
        url(r'^new2/$', views.new_exp,{}, name='new2'),
        url(r'^edit2/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.new_exp,{}, name='edit'),
	url(r'^delete2/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.new_exp,{}, name='delete'),        
	
	url(r'^(?P<mode>new)/$', views.new_exp2,{}, name='new'),
	url(r'^(?P<mode>edit)/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.new_exp2,{}, name='edit2'),
	url(r'^delete/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.new_exp2,{}, name='delete2'),
	url(r'^finish/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.finish_exp,{}, name='finish'),

	url(r'^new/example', views.new_exp_example, name='new_example'),
	##############################detail############################
	url(r'^get/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?P<mode>\w+)/$', views.add_edit_sample,{}, name='addsample'),
	url(r'^get/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?P<mode>\w+)/(?P<sample_id>\d+)/$', views.add_edit_sample,{}, name='editsample'),
	
	url(r'^get/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',views.detail, name='detail'),
	#LOG
	url(r'^get/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/log/(?P<mode>\w+)/$',views.new_edit_log, name='new_log'),
	

	#####################Import and Export###########################
	url(r'^export/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/samplesheet/$', views.export_samplesheet_csv,{}, name='export'),
	url(r'^export/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/log/$', views.export_log,{}, name='export'),
	url(r'^import/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.import_samplesheet_csv,{}, name='import'),
	
	
	#url(r'^export/(?P<original_filename>.+)$', views.respond_as_attachment,{}, name='export_db'),

	#####################Info and confirm ###########################
	url(r'^(?P<mode>new)/confirm/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.confirm, name='new_confirm'),
	url(r'^(?P<mode>delete)/confirm/(?P<experiment_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.confirm, name='del_confirm'),

	
	url(r'^search/$', views.planned, name='planned'),
	#url(r'^signup/$', views.signup, name='signup'),
	#url(r'^login/$', views.login, name='login'),

	#########################USER CONSOLE############################
	url(r'^console/$', views.console, name='console'),
	url(r'^console/log/$', views.log, name='log'),
	url(r'^console/myexperiments/$', views.myexperiments, name='myexperiments'),
	url(r'^console/account/$', views.account, name='account'),

	url(r'finished/$', views.physical_search, name='physical_search'),

	##########################database views##########################
	url(r'^investigators/$', views.IDMSUserList.as_view(template_name='dbView/IDMSUserList.html')),
	url(r'^cclelibrary/$', views.CcleLibraryList.as_view(template_name='dbView/CcleLibraryList.html')),
	url(r'^miseqindex/$', views.MiseqIndexList.as_view(template_name='dbView/MiseqIndexList.html')),
	url(r'^shrnalibrary/$', views.ShrnaLibraryList.as_view(template_name='dbView/ShrnaLibraryList.html')),
	url(r'^treatments/$', views.TreatmentList.as_view(template_name='dbView/TreatmentList.html')),

]
