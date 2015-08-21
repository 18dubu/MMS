# -*- coding: utf-8 -*-
from .models import Experiment, Sample, Log, IDMSUser,MiseqIndex,PoolNumberChoice,Treatment,CcleLibrary,ShrnaLibrary, Project, FinishedMiseq
from forms import ExperimentForm, SampleForm, SampleFormSet, SampleFormSetP, SampleFormSet0, SampleFormSet0P, SampleSheetImportForm, LogForm,FinishForm

from django.views.generic import ListView
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.template.defaulttags import register
from django.utils import timezone
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
import uuid
import csv
import time
from datetime import datetime


'''
def Experiment_asJson(request):
    object_list = MiseqIndex.objects.all() #or any kind of queryset
    #j = json.dumps(object_list)
    
    
    j = json.dumps([ob.as_json() for ob in object_list])

    #js = serializers.serialize('json', object_list)
    return HttpResponse(j, content_type='application/json')
    #return render_to_response('listView/ajax_search.html', 
    #                      {'experimentResponse': json})
    #return render_to_response('listView/ajax_search.html',{'experiments' : j})    
'''
#alert banner on detail page
def get_alert(experiment):
	alert = ''
	exp = experiment
	overdue_template = "<div class=\"alert alert-dismissible alert-danger\">\
			  <button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>\
			  <h4>This Experiment is Overdue!</h4>\
			  <p>If it has been conducted, you can <a href=\"/virtual/finish/%s/\" class=\"alert-link\">change its status to \"finished\"</a>.</p>\
			</div>"

	finish_template = "\
			<div class=\"alert alert-dismissible alert-success\">\
                        <button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>\
			<h4>This Experiment is marked as finished!</h4>\
			 <p>If the status is not correct, you can <a href=\"/virtual/finish/%s/\" class=\"alert-link\">edit the status</a>.</p>\
			</div>"

	upcoming_template = "\
                        <div class=\"alert alert-dismissible alert-warning\">\
                        <button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>\
			<h4>This Experiment is due in the coming days!</h4>\
                        <p>If it has been conducted, you can <a href=\"/virtual/finish/%s/\" class=\"alert-link\">change its status to \"finished\"</a>.</p>\
                        <p>Otherwise, you can <a href=\"/virtual/edit/%s/\" class=\"alert-link\">edit the experiment</a>.</p>\
                        </div>"


	#overdue
	now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
	if exp.experiment_date < now and exp.finish_flag != 'Finished' and exp.finish_flag != "Submitted" and exp.finish_flag != "Analyzing":
		alert = overdue_template % exp.experiment_id.decode('utf-8').encode('utf-8')
	#finished
	if exp.finish_flag == 'Finished' or exp.finish_flag == "Submitted" or exp.finish_flag == "Analyzing":
		alert = finish_template % (exp.experiment_id.decode('utf-8').encode('utf-8'))
	#upcoming
	if exp.finish_flag != 'Finished'and exp.finish_flag != "Submitted" and exp.finish_flag != "Analyzing" and exp.experiment_date > now:
		delta = exp.experiment_date - now
		if delta.days < 2: # due in two days
			alert = upcoming_template % (exp.experiment_id.decode('utf-8').encode('utf-8'),exp.experiment_id.decode('utf-8').encode('utf-8'))
	#analysis
	#TODO

	return alert

def get_auth_users(experiments):
	auth_users = {}
        for e in experiments:
                curr = []
                for i in e.investigator.all():
                        curr.append(i.NTID.upper())
		#append admin to all experiments
		curr.append('ADMIN')
		curr.append(e.created_by.NTID.upper())
                auth_users[e.experiment_id] = curr

	return auth_users


#experiment should be sorted by conducting date
def get_dashboard_data(experiments):
	todo = ''
	finish = ''
	calendar = '['
	todo_template = "<li>\
                      <span class=\"handle\">\
                        <i class=\"fa fa-ellipsis-v\"></i>\
                        <i class=\"fa fa-ellipsis-v\"></i>\
                      </span>\
                      <input type=\"checkbox\" value=\"\" name=\"\" />\
                      <span class=\"text\"><strong>Project: </strong> %s <strong>&nbsp;&nbsp;Experiment: </strong><a href=\"%s\">%s</a></span>\
                      <small class=\"label %s\"><i class=\"fa fa-clock-o\"></i> %s </small>\
                    </li>\
"
        finish_template = "<tr>\
                          <td>%s</td>\
                          <td><a href=\"%s\">%s</a></td>\
                          <td>%s</td>\
                          <td>%s</td>\
                        </tr>\
        "

	calendar_template = "{title: '%s',start: new Date(y%s, m%s, d%s),url: '%s',backgroundColor: \"%s\",borderColor: \"%s\"},"

	labels = ['label-danger','label-warning','label-primary','label-info','label-default','label-success']	
	colors = ['#f56954','#f39c12','#3c8dbc','#00c0ef','#0073b7','#00a65a']
	j=0
	k=0
	limit=8
	due_in_two_days = 0
	for exp in experiments:
		now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
			
		#finish list
		if exp.finish_flag == 'Submitted' and j<=limit:
                        j+=1
                        if exp.feedback_flag == 'Negative':
                                info = "<small class=\"label label-danger\"><i class=\"fa ion-flag\"></i> Negative </small>"
                        elif exp.feedback_flag == 'Positive':
                                info = "<small class=\"label label-success\"><i class=\"fa ion-flag\"></i> Positive </small>"
                        elif exp.feedback_flag == 'Questionable':
                                info = "<small class=\"label label-warning\"><i class=\"fa ion-flag\"></i> Questionable </small>"
                        else:
                                info = ''
                        tmp1 = finish_template % (exp.get_taged_project_name,exp.get_absolute_url,exp.title,exp.comment,info)
                        finish += tmp1

		#todo list
		if exp.experiment_date > now and exp.finish_flag != 'Submitted':
			delta = exp.experiment_date - now
			k+=1		
			if delta.days < 2: #two days
				i = 1
				due_in_two_days += 1
				info = str(delta.seconds/3600) + ' hours'
			elif delta.days < 5: #five days
                                i = 2
				info = str(delta.days) + ' days'
			elif delta.days < 10: #10 days
                                i = 3
				info = str(delta.days) + ' days'
			elif delta.days < 30: #30 days
                                i = 4
				info = str(delta.days/7) + ' weeks'
			else:
                                i = 4
				info = str(delta.days/(30)) + ' months'
			if (k < limit):
				tmp2 = todo_template % (exp.get_taged_project_name,exp.get_absolute_url,exp.title, labels[i], info)
				todo += tmp2
		#calendar
		else:
			if exp.finish_flag == 'Submitted':
				i= 5
			else:
				i= 0
		y_delta = exp.experiment_date.year - now.year
		m_delta = exp.experiment_date.month - now.month
		d_delta = exp.experiment_date.day - now.day
		if y_delta==0: y_delta=''
		elif y_delta>0: y_delta='+'+str(y_delta)
		elif y_delta<0: y_delta=str(y_delta)
		if m_delta==0: m_delta=''
		elif m_delta>0: m_delta='+'+str(m_delta)
		elif m_delta<0: m_delta=str(y_delta)
		if d_delta==0: d_delta=''
		elif d_delta>0: d_delta='+'+str(d_delta)
		elif d_delta<0: d_delta=str(d_delta)
		
		calendar += calendar_template %(exp.title,y_delta,m_delta,d_delta,exp.get_absolute_url,colors[i],colors[i])
	calendar += ']'
	return todo,due_in_two_days,calendar,finish
	
def get_finished_list_html(experiments):
        content = ''
        template = "<tr>\
                          <td>%s</td>\
                          <td><a href=\"%s\">%s</a></td>\
                          <td>%s</td>\
			  <td>%s</td>\
                        </tr>\
	"
        j=0
	limit=8
	for exp in experiments:
                if exp.finish_flag == 'Finished' and j<=limit:
			j+=1
			if exp.feedback_flag == 'Negative':
				info = "<small class=\"label label-danger\"><i class=\"fa ion-flag\"></i> Negative </small>"
			elif exp.feedback_flag == 'Positive':
                                info = "<small class=\"label label-success\"><i class=\"fa ion-flag\"></i> Positive </small>"
			elif exp.feedback_flag == 'Questionable':
                                info = "<small class=\"label label-warning\"><i class=\"fa ion-flag\"></i> Questionable </small>"
			else:
				info = ''
                        tmp = template % (exp.get_taged_project_name,exp.get_absolute_url,exp.title,exp.comment,info)
                        content += tmp

        return content

	

###############################################################

def planned(request):
	experiments = Experiment.objects.all()

	args = {}
        args.update(csrf(request))
        args['p'] = request.GET.get('p', '')
	args['u'] = request.GET.get('u', '')
	args['experiments'] = experiments
        args['user'] = request.user
        args['auth_users'] = get_auth_users(experiments)

	return render_to_response('listView/planned.html', args)


def physical_search(request):
        experiments = FinishedMiseq.objects.all()
        args = {}
        args.update(csrf(request))
        args['p'] = request.GET.get('p', '')
        args['u'] = request.GET.get('u', '')
        args['user'] = request.user
        args['experiments'] = experiments

        return render_to_response('listView/finished.html', args)


'''
class OrderListJson(BaseDatatableView):
    model = MiseqIndex
    columns = ['id', 'index']
    order_columns = ['id','index']
    max_display_length = 100

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        return MiseqIndex.objects.all()

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        # simple example:
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(index__istartswith=search)

        # more advanced example
	
        filter_customer = self.request.GET.get(u'customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
     
	else:
		pass
	
	return qs


    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.index,
            ])
        return json_data

'''

def index(request):
	#experiments = Experiment.objects.all()
	experiments = Experiment.objects.order_by('-created_date')

        args = {}
        args.update(csrf(request))
        args['user'] = request.user
        args['experiments'] = experiments
	args['auth_users'] = get_auth_users(experiments)
	return render_to_response('listView/front.html',args)
	

def detail(request, experiment_id):
	experiment = get_object_or_404(Experiment, experiment_id=experiment_id)
	posts = Log.objects.filter(related_exp=experiment)

	args = {}
        args.update(csrf(request))
        args['user'] = request.user
        args['experiment'] = experiment
	args['auth_users'] = get_auth_users([experiment])
	args['posts'] = posts
	args['alert'] = get_alert(experiment)
	
	if request.POST.get('delete_sam'):
                Sample.objects.filter(pk=request.POST.get('delete_sam')).delete()
                #experiment.sample_set.remove(sam2delete)
                #return render_to_response(request, 'detailView/detail.html', args)
                return HttpResponseRedirect('/virtual/get/%s/#sample' % experiment.experiment_id)

	else:
		return render(request, 'detailView/detail.html', args)


def new_exp(request, experiment_id=None):
	def generate_sample_name(sample):

                '''
                naming standard:
                CellLine.Library.TreatmentIfAny.shON/shOFF.time.A/B/C
                Example: A549.K1_2.EZH2_150nM.shON.T21.A
                '''
		sample_name = ".".join([sample.cell_model.CCLE_name,sample.shRNA_library.LibName])
		
		#if sample.pool_number is not None:
		#	pool_str = '_P'
		#	tmp = ''
			#for p in sample.pool_number():
			#	tmp += '_'+p.description
			#pool_str += tmp[1:]
		#else:
		#	pool_str = '_PNone'
		
		#sample_name = sample_name + pool_str	
	
		if sample.treatment and sample.treatment_dose:
			treatment = '_'.join([sample.treatment.compoundName,str(sample.treatment_dose)])
                	sample_name = '.'.join([sample_name,treatment])
		shrna = 'shON'
                if not sample.shRNA_on:
                        shrna = 'shOFF'

		time = ''.join(['T',str(sample.time_in_days)])
		if sample.environment == 'inVivo':
			time = 'inVivo'

		sample_name = '.'.join([sample_name,shrna,sample.environment,sample.replicate])
		
                if sample.other_tag:
                        sample_name = sample_name + '.' + sample.other_tag
                return sample_name

	if experiment_id:
		experiment = get_object_or_404(Experiment, experiment_id=experiment_id)
		expform = ExperimentForm(instance=experiment)
                samforms = SampleFormSet(instance=experiment)
		#if experiment.user != request.user:
#		return HttpResponseForbidden()
	else:
		experiment = Experiment()#(user=request.user)
	
	if request.POST:
		if 'create_exp' in request.POST or 'add_sample' in request.POST:
			expform = ExperimentForm(request.POST, instance=experiment)
			samforms = SampleFormSet(request.POST, instance=experiment)
			if expform.is_valid() and samforms.is_valid():
				new_exp = expform.save(commit=False)
			
				#automatic generate or modify fields
				#save modified form
				new_exp.save()
				expform.save_m2m()				
				#sample forms
				samforms.instance = new_exp
				if samforms.has_changed():	
					for samform in samforms:
						if samform.is_valid() and samform.has_changed() and (samform is not None):
							new_sam = samform.save(commit=False)
							#new_sam.pool_number = samform.cleaned_data['pool_number']
							#new_sam.sample_id = experiment.sample_set.count() + 1
							new_sam.sample_name = generate_sample_name(new_sam)
						#	new_sam.save()
						#	samform.save_m2m()
					new_sam = samforms.save()
				return HttpResponseRedirect('/virtual/new/confirm/%s/' % new_exp.experiment_id)
		elif 'delete_exp' in request.POST:
			exp2delete = get_object_or_404(Experiment, experiment_id=experiment.experiment_id).delete()
			#return HttpResponseRedirect('/virtual/delete/%s/' % experiment.experiment_id)
			return HttpResponseRedirect('/virtual/new/confirm/%s/' % experiment.experiment_id)		
	else:
		expform = ExperimentForm(instance=experiment)
		samforms = SampleFormSet(instance=experiment)

	args = {}
	args.update(csrf(request))
	args['expform'] = expform
	args['samforms'] = samforms
	args['user'] = request.user
	return render_to_response('newExpView/new.html',args)

@login_required
def new_exp2(request, mode, experiment_id=None):

	if experiment_id:
                experiment = get_object_or_404(Experiment, experiment_id=experiment_id)
		expform = ExperimentForm(instance=experiment)
                #if experiment.user != request.user:
#               return HttpResponseForbidden()
        else:
                experiment = Experiment()#(user=request.user)

        if request.POST:
                if 'next' in request.POST:
                        expform = ExperimentForm(request.POST, instance=experiment)
					
			if expform.is_valid():
                          	new_exp = expform.save(commit=False)

                   	        #automatic generate or modify fields
                                #save modified form
				try:
					new_exp.created_by = IDMSUser.objects.get(NTID__iexact=request.user.username)
                      		except:
					raise Exception("can not find"+request.user.username+'in IDMS db error')
				new_exp.save()
                               	expform.save_m2m()
                                #sample forms
				return HttpResponseRedirect('/virtual/get/%s/' % new_exp.experiment_id)
			else:
				raise Exception('Form not valid')
		elif 'delete_exp' in request.POST:
			if experiment_id is not None:
                        	exp2delete = get_object_or_404(Experiment, experiment_id=experiment.experiment_id).delete()
                        	if request.user.is_authenticated():
					return HttpResponseRedirect('/virtual/console/')	
				else:
					return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/')
        	elif 'cancel_exp' in request.POST:
			return HttpResponseRedirect('/')

        else:
		expform = ExperimentForm(instance=experiment)
		
        args = {}
        args.update(csrf(request))
        args['expform'] = expform
	args['mode'] = mode
	args['user'] = request.user
        return render_to_response('newExpView/new2.html',args)


@login_required
def finish_exp(request, experiment_id=None):
        if experiment_id:
                experiment = get_object_or_404(Experiment, experiment_id=experiment_id)
		if  request.user.username.upper() in get_auth_users([experiment])[experiment_id]:
			if request.POST:
				if 'submit' in request.POST:
					finishform = FinishForm(request.POST, instance=experiment)	
					if finishform.is_valid():
		                                new_exp = finishform.save(commit=False)
		                                new_exp.finish_flag = new_exp.finish_flag
						new_exp.save()
						#send email
						if new_exp.finish_flag=='Finished' and new_exp.miseq_folder_name and new_exp.analyst:

							#try:
								
							send_mail('MMS Request Analysis', ' '.join([experiment_id,new_exp.miseq_folder_name]), request.user.username,['handong.ma@pfizer.com'], fail_silently=False)
							return HttpResponseRedirect('/virtual/new/confirm/%s/' % new_exp.experiment_id)								
							#except:
							#	return HttpResponseRedirect('/virtual/get/%s/' % new_exp.experiment_id)
							#	raise Exception('Send email error')
		
	                                	return HttpResponseRedirect('/virtual/get/%s/' % new_exp.experiment_id)


				
				elif 'cancel' in request.POST:
                        		return HttpResponseRedirect('/virtual/get/%s/' % experiment.experiment_id)
			else:
				finishform = FinishForm(instance=experiment)
		else:
			raise PermissionDenied()
        else:
                return HttpResponseRedirect('/1')


        args = {}
        args.update(csrf(request))
	args['experiment'] = experiment
        args['finishform'] = finishform
        args['user'] = request.user
        return render_to_response('detailView/finish.html',args)



def add_edit_sample(request,experiment_id, mode,sample_id=None):
        def generate_sample_name(sample):

                '''
                naming standard:
                CellLine.Library.TreatmentIfAny.shON/shOFF.time.A/B/C
                Example: A549.K1_2.EZH2_150nM.shON.T21.A
                '''
                sample_name = ".".join([sample.cell_model.CCLE_name,sample.shRNA_library.LibName])

                if len(sample.pool_number.all())>0:
                	pool_str = '_P'
                      	tmp = ''
                       	for p in sample.pool_number.all():
                		if not tmp:
					 tmp = p.description
				else:
					tmp = '_'+p.description
                        	pool_str += tmp
                else:
                      	 pool_str = '_PNone'

                sample_name = sample_name + pool_str

                if sample.treatment and sample.treatment_dose:
                        treatment = '_'.join([sample.treatment.compoundName,str(sample.treatment_dose)])
                        sample_name = '.'.join([sample_name,treatment])
                shrna = 'shON'
                if not sample.shRNA_on:
                        shrna = 'shOFF'

        	time = ''.join(['T',str(sample.time_in_days)])
                if sample.environment == 'inVivo':
                        time = 'inVivo'

	        sample_name = '.'.join([sample_name,shrna,time,sample.replicate])

                if sample.other_tag:
                        sample_name = sample_name + '.' + sample.other_tag
                return sample_name

	experiment = get_object_or_404(Experiment, experiment_id=experiment_id)	
	title=''
	if request.POST:
		if request.POST.get('cancel_sam', None):
			return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload(true);</script>')	

		samforms = SampleFormSet(request.POST,instance=experiment)	
		
		if samforms.is_valid():
			if 1:#samforms.has_changed():
				for samform in samforms:
					if  mode == 'editsample':
						if samform.has_changed() and samform is not None:
							if samform.is_valid():
								new_sam = samform.save(commit=False)
								new_sam.save()
								samform.save_m2m()		
								new_sam.sample_name = generate_sample_name(new_sam)
								new_sam.save()
					if mode == 'addsample':
						if samform.is_valid() and samform.has_changed() and samform is not None:
                                                        new_sam = samform.save(commit=False)
                                                        new_sam.save()
                                                        samform.save_m2m()
                                                        new_sam.sample_name = generate_sample_name(new_sam)
                                                        new_sam.save()

				
				return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload(true);</script>')
	
	else:
	        if mode == 'addsample':
        	        title = 'Add Sample'
                	if sample_id is None:
                        	samforms = SampleFormSet()
               		else:
				targetSam = get_object_or_404(experiment.sample_set.all(),pk=sample_id)
				init_data = {'cell_model':targetSam.cell_model,
						'shRNA_on':targetSam.shRNA_on,
						'shRNA_library':targetSam.shRNA_library,
						'time_in_days':targetSam.time_in_days,
					#	'pool_number':targetSam.pool_number,
						'treatment':targetSam.treatment,
						'treatment_dose':targetSam.treatment_dose,
						#'replicate':targetSam.replicate,
						'other_tag':targetSam.other_tag,
						'comment':targetSam.comment
						}
				samforms = SampleFormSetP(instance=Experiment(),initial=[init_data],sample_id=sample_id)

		elif mode == 'editsample':
			title = 'Edit Sample'
			if sample_id is None:	
				samforms = SampleFormSet0(instance=experiment)
			else:
				targetSam = get_object_or_404(experiment.sample_set.all(),pk=sample_id)
			#	samforms = SampleForm(instance=Sample.objects.filter(id=sample_id),sample_id=sample_id)
				samforms = SampleFormSet0P(instance=experiment, queryset=Sample.objects.filter(id=sample_id),sample_id=sample_id)
		else:
			raise Exception('Unknow URL parameter')

        args = {}
        args.update(csrf(request))
        args['experiment_id'] = experiment_id
	args['sample_id'] = sample_id
	args['title'] = title
        args['samforms'] = samforms
	args['user'] = request.user
	return render_to_response('newExpView/sample.html',args)



def new_exp_example(request):
	return render(request, 'newExpView/example.html')
	


def confirm(request,mode,experiment_id):
	if mode == 'new':
		title = 'Create New Experiment'
	if mode == 'delete':
		title = 'Delete Experiment'

	args = {}
	args.update(csrf(request))
	args['experiment_id'] = experiment_id
	args['title'] = title
	args['mode'] = mode
	args['user'] = request.user
	return render_to_response('newExpView/confirm.html',args)
		

def export_samplesheet_csv(request,experiment_id):
	curr_exp = get_object_or_404(Experiment, experiment_id=experiment_id)
	response = HttpResponse(content_type='text/csv')
    	response['Content-Disposition'] = 'attachment; filename="SampleSheet_%s.csv"' % experiment_id
	writer = csv.writer(response)
    	writer.writerow(['[Header]','','','','','','','',''])
    	writer.writerow(['IEMFileVersion',curr_exp.version,'','','','','','',])
	writer.writerow(['Investigator Name',curr_exp.get_comma_separated_investigator_name])
	writer.writerow(['Experiment Name',curr_exp.title])
	writer.writerow(['Date',curr_exp.experiment_date.date()])
	writer.writerow(['Workflow',curr_exp.workflow])
	writer.writerow(['Application',curr_exp.application])
	writer.writerow(['Assay',curr_exp.assay])
	writer.writerow(['Description',curr_exp.description])
        writer.writerow(['Chemistry',curr_exp.chemistry])
        writer.writerow([])
        writer.writerow(['[Reads]'])
        writer.writerow([curr_exp.reads])
        writer.writerow([])
        writer.writerow(['[Settings]'])
        writer.writerow(['ReverseComplement',curr_exp.reverse_complement])
        writer.writerow([])
        writer.writerow(['[Data]'])
        writer.writerow(['Sample_ID','Sample_Name','Sample_Plate','Sample_Well','I7_Index_ID','index','Sample_Project','Description','group','cell_model','shRNA_library','pool_number','shRNA_on','time_in_days','treatment','treatment_dose (nM)','replicate','other_tag','comment','finish_flag'])
	sample_id = 0
	for sample in curr_exp.sample_set.all().order_by('created_date'):
		group = sample.sample_name.split('.')
		group.pop()
		sample_id += 1
		treatment = ''
		treatment_dose = ''
		if sample.treatment is not None:
			treatment = sample.treatment.compoundName
		if sample.treatment_dose is not None:
                        treatment_dose = str(sample.treatment_dose)

		writer.writerow(['S'+str(sample_id),sample.sample_name,'','',sample.index.I7_Index_ID,sample.index.index,curr_exp.title,curr_exp.description,'.'.join(group),sample.cell_model.CCLE_name,sample.shRNA_library.LibName,sample.get_pool_numbers_display,sample.get_shRNA_on_display(),sample.time_in_days,treatment,treatment_dose,sample.replicate,sample.other_tag,sample.comment,sample.finish_flag])

    	return response


def import_samplesheet_csv(request,experiment_id):
	if request.method == 'POST':
        	form = SampleSheetImportForm(request.POST, request.FILES)
        	if form.is_valid():
            		handle_uploaded_file(request.FILES['file'])
            		return HttpResponseRedirect('/success/url/')
    	else:
        	form = SampleSheetImportForm()
    	return render_to_response('detailView/upload.html', {'form': form})


def export_log(request,experiment_id):
        curr_exp = get_object_or_404(Experiment, experiment_id=experiment_id)
	#IDMSUser.objects.get(NTID__iexact=request.user.username)
	#curr_exp.download_date = datetime.now()
	#curr_exp.save()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ExpermentLog_%s.csv"' % experiment_id
        writer = csv.writer(response)
	writer.writerow(['Log_ID','subject','content','writer','visible_to','created_date','created_by','updated_date','updated_by','download_date','download_by'])
        log_id = 0
	posts = Log.objects.filter(related_exp=curr_exp)
        if posts:
		for log in posts:
			log_id += 1
			log.download_date = datetime.now()
			log.download_by = IDMSUser.objects.filter(NTID__iexact=request.user.username)
			log.save()
			writers=[]
			for w in log.writer.all():
				writers.append(w.NTID)
			writer.writerow(['L'+str(log_id),log.subject,log.content,'/'.join(writers),log.visible_to,log.created_date,'',log.updated_date,'',datetime.now(),request.user.username])#TODO

        return response



#https://djangosnippets.org/snippets/1710/
def respond_as_attachment(request, original_filename, media_path='media/'):
    from urlparse import urlparse
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(request.build_absolute_uri()))
    file_path = domain + media_path + original_filename[:-1]
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response




def signup(request):
	return render_to_response('signView/signup.html')

@login_required
def console(request):
	
	experiments = Experiment.objects.filter(Q(investigator__NTID__iexact=request.user.username) | Q(created_by__NTID__iexact=request.user.username)).distinct().order_by('experiment_date')
	
	idms = IDMSUser.objects.get(NTID__iexact=request.user.username)	
        posts = Log.objects.filter(created_by__NTID__iexact=request.user.username).order_by('-created_date')
	
	args = {}
        args.update(csrf(request))
        args['user'] = request.user
	args['experiments'] = experiments
	args['auth_users'] = get_auth_users(experiments)
        args['idms'] = idms
	todo,due_in_2,calendar,finished = get_dashboard_data(experiments)
	args['todo'] = todo
	args['due_in_2'] = due_in_2

	args['calendar_data'] =  calendar
	args['finished'] = finished#get_finished_list_html(experiments)
	args['posts'] = posts	

	return render_to_response('consoleView/account.html',args)

@login_required
def myexperiments(request):
        experiments = Experiment.objects.filter(investigator__NTID__iexact=request.user.username).order_by('-created_date')
	args = {}
        args.update(csrf(request))
        args['experiments'] = experiments
	args['user'] = request.user
	return render_to_response('consoleView/myexperiments.html',args)
	

@login_required
def log(request):
        experiments = Experiment.objects.filter(investigator__NTID__iexact=request.user.username).order_by('-created_date')
        posts = Log.objects.filter(created_by__NTID__iexact=request.user.username).order_by('-created_date')
	args = {}
        args.update(csrf(request))
        args['experiments'] = experiments
        args['user'] = request.user
	args['posts'] = posts
        return render_to_response('consoleView/logFront.html',args)


@login_required
def new_edit_log(request, mode, experiment_id=None):

        if experiment_id:
                experiment = get_object_or_404(Experiment, experiment_id=experiment_id)
                log = Log(related_exp=experiment)
                #if experiment.user != request.user:
#               return HttpResponseForbidden()
        else:
                log = Log()

        if request.POST:
                if 'create_log' in request.POST:
                        logform = LogForm(request.POST, instance=log)

                        if logform.is_valid():
                                new_log = logform.save(commit=False)

                                #automatic generate or modify fields
                                #save modified form
                                new_log.created_by = IDMSUser.objects.get(NTID__iexact=request.user.username)
				new_log.save()
                                logform.save_m2m()
                                #sample forms

                                return HttpResponseRedirect('/virtual/get/%s/' % experiment.experiment_id)

                elif 'delete_log' in request.POST:
                        if experiment_id is not None:
				if experiment_id:
                                	log2delete = get_object_or_404(Log, related_exp=experiment).delete()
					return HttpResponseRedirect('/virtual/get/%s/' % experiment.experiment_id)
                        else:
                                return HttpResponseRedirect('/')
                elif 'cancel_log' in request.POST:
                        return HttpResponseRedirect('/')

        else:
                logform = LogForm(instance=log)

        args = {}
        args.update(csrf(request))
        args['logform'] = logform
        args['mode'] = mode
        args['user'] = request.user
        return render_to_response('newExpView/log.html',args)




@login_required
def account(request):
        experiments = Experiment.objects.filter(investigator__NTID__iexact=request.user.username).order_by('-created_date')
        args = {}
        args.update(csrf(request))
        args['experiments'] = experiments
        args['user'] = request.user
        return render_to_response('consoleView/userConsole.html',args)





class IDMSUserList(ListView):
	model = IDMSUser

class CcleLibraryList(ListView):
        model = CcleLibrary

class MiseqIndexList(ListView):
        model = MiseqIndex

class ShrnaLibraryList(ListView):
        model = ShrnaLibrary


class TreatmentList(ListView):
        model = Treatment



######################registered template filters##########################
#{{ mydict|get_item:item.NAME }}
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def key(d, key_name):
    try:
        value = d[key_name]
    except:
        from django.conf import settings

        value = settings.TEMPLATE_STRING_IF_INVALID

    return value


