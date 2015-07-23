# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Experiment, Sample, IDMSUser,MiseqIndex
from django.template import RequestContext, loader
from django.utils import timezone
from django.core.context_processors import csrf
from forms import ExperimentForm, SampleForm, SampleFormSet,SampleSheetImportForm
from django_datatables_view.base_datatable_view import BaseDatatableView
import time
from django.forms.models import model_to_dict
import json
import uuid
import csv




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

def datatable(request):
	args = {}
        args.update(csrf(request))
        args['p'] = request.GET.get('p', '')
	args['u'] = request.GET.get('u', '')
	args['experiments'] = Experiment.objects.all()
        return render_to_response('listView/datatable.html', args)


def physical_search(request):
        experiments = Experiment.objects.all()
        return render_to_response('listView/datatable.html', {'experiments':experiments})


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
	experiments = Experiment.objects.order_by('-created_date')[:1000]
	return render_to_response('listView/front.html', {'experiments':experiments})
	

def detail(request, experiment_id):
	experiment = get_object_or_404(Experiment, experiment_id=experiment_id)
	return render(request, 'detailView/detail.html', {'experiment': experiment})

#popupnew
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
		sample_name = '.'.join([sample_name,shrna,''.join(['T',str(sample.time_in_days)]),sample.replicate])
		
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
	return render_to_response('newExpView/new.html',args)

def new_exp_example(request):
	return render(request, 'newExpView/example.html')
	


def new_confirm(request,experiment_id):
	return render_to_response('newExpView/confirm.html',{'experiment_id': experiment_id})

def export_csv(request,experiment_id):
	curr_exp = get_object_or_404(Experiment, experiment_id=experiment_id)
	response = HttpResponse(content_type='text/csv')
    	response['Content-Disposition'] = 'attachment; filename="SampleSheet_%s.csv"' % experiment_id
	writer = csv.writer(response)
    	writer.writerow(['[Header]','','','','','','','',''])
    	writer.writerow(['IEMFileVersion',curr_exp.version,'','','','','','',])
	writer.writerow(['Investigator Name'])
	writer.writerow(['Experiment Name',curr_exp.title])
	writer.writerow(['Date',curr_exp.experiment_date])
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
        writer.writerow(['Sample_ID','Sample_Name','Sample_Plate','Sample_Well','I7_Index_ID','index','Sample_Project','Description','group'])
	sample_id = 0
	for sample in curr_exp.sample_set.all().order_by('created_date'):
		group = sample.sample_name.split('.')
		group.pop()
		sample_id += 1
		writer.writerow(['S'+str(sample_id),sample.sample_name,'','',sample.index.I7_Index_ID,sample.index.index,curr_exp.title,curr_exp.description,'.'.join(group)])

    	return response


def import_csv(request,experiment_id):
	if request.method == 'POST':
        	form = SampleSheetImportForm(request.POST, request.FILES)
        	if form.is_valid():
            		handle_uploaded_file(request.FILES['file'])
            		return HttpResponseRedirect('/success/url/')
    	else:
        	form = SampleSheetImportForm()
    	return render_to_response('detailView/upload.html', {'form': form})

'''
def search_title(request):
	if request.method == 'POST':
		search_text = request.POST['search_text']
	else:
		search_text = ''

	experiments = Experiment.objects.filter(title__contains=search_text)
	
	return render_to_response('listView/ajax_search.html',{'experiments' : experiments})
'''

def signup(request):
	return render_to_response('signView/signup.html')

def login(request):
        return render_to_response('signView/login.html')

def console(request):
        return render_to_response('consoleView/userConsole.html')









