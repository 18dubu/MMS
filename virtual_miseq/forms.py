from django import forms
from models import Experiment, Sample, Log, Project
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets     
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError                   
from parsley.decorators import parsleyfy

import selectable.forms as selectable
from selectable.forms import AutoCompleteWidget

from .lookups import InvestigatorLookup,CellmodelLookup, ShrnaLookup, ExperimentTitleLookup, ProjectLookup

from .models import IDMSUser

#http://blog.brendel.com/2012/01/django-modelforms-setting-any-field.html
class ExtendedMetaModelForm(forms.ModelForm):
    """
    Allow the setting of any field attributes via the Meta class.
    """
    def __init__(self, *args, **kwargs):
        """
        Iterate over fields, set attributes from Meta.field_args.
        """
        super(ExtendedMetaModelForm, self).__init__(*args, **kwargs)
        if hasattr(self.Meta, "field_args"):
            # Look at the field_args Meta class attribute to get
            # any (additional) attributes we should set for a field.
            field_args = self.Meta.field_args
            # Iterate over all fields...
            for fname, field in self.fields.items():
                # Check if we have something for that field in field_args
                fargs = field_args.get(fname)
                if fargs:
                    # Iterate over all attributes for a field that we
                    # have specified in field_args
                    for attr_name, attr_val in fargs.items():
                        if attr_name.startswith("+"):
                            merge_attempt = True
                            attr_name = attr_name[1:]
                        else:
                            merge_attempt = False
                        orig_attr_val = getattr(field, attr_name, None)
                        if orig_attr_val and merge_attempt and \
                                    type(orig_attr_val) == dict and \
                                    type(attr_val) == dict:
                            # Merge dictionaries together
                            orig_attr_val.update(attr_val)
                        else:
                            # Replace existing attribute
                            setattr(field, attr_name, attr_val)



@parsleyfy
class ExperimentForm(forms.ModelForm):
	error_css_class = 'error'
    	required_css_class = 'required'	
	class Meta:
		model = Experiment
		#fields = '__all__'
		exclude = ('experiment_id','feedback_flag','finish_flag','created_by','created_date','updated_by','updated_date','download_by','download_date','comment','design_type','miseq_folder_name')
		#fields = ('project_name','title','experiment_date','investigator','description','reads','workflow','chemistry','application','assay','version','reverse_complement',)
		

		widgets = {
            		'experiment_date': forms.DateInput(attrs={'class':'datepicker'}),
        	}

		labels = {
			'title': 'Title (Experiment Name)',
			'experiment_date':'Date to run MiSeq',
			'description': mark_safe('Description (sufficient information for this screen, (<a href="/virtual/new/example/#desc" target="_blank">Example</a>)'),
		}
		
		#help_texts = {
		#	'experiment_id': 'Unique Experiment ID, No need to modify',
		#	'experiment_date': 'Scheduled Experiment date',
		#	'version': 'Default Version 4, can be modified',
		#}
		
		#https://docs.djangoproject.com/en/dev/ref/forms/api/#styling-required-or-erroneous-form-rows	
		error_messages = {
			'title': {'required':('How should I call you, my Experiment?'),},
			'project_name' : {'required':('A project organizes related Experiments!'),},
			'description': {'required':('Some words for reference'),},
			'experiment_date': {'required':('Let\' make a schedule'),},
			NON_FIELD_ERRORS: {
                		'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            		}
		}
		

		parsley_extras = {
     	   	'project_name': {
        	    	'minlength': '2',
            		'error-message': 'Category is required.',
        },
    }

	investigator = selectable.AutoCompleteSelectMultipleField(
	    	lookup_class=InvestigatorLookup,
		label='Investigator (Type to search)',
	    	required=True,
		error_messages={'required':('Guy(s) who will conduct the experiment'),},
	)

	title = forms.CharField(
	        widget = AutoCompleteWidget(ExperimentTitleLookup),        
		label='Experiment Title (Search or Add New)',
                required=True,
                error_messages={'required':('How should I call you, my Experiment?'),},
        )
	

	project_name = forms.CharField(
		widget = AutoCompleteWidget(ProjectLookup),
                label='Project Name (Search or Add New)',
                required=True,
		error_messages={'required':('A project organizes related Experiments!'),},
        )

	def __init__(self, *args, **kwargs):
        	#user = kwargs.pop('user','')
        	
		super(ExperimentForm, self).__init__(*args, **kwargs)
		#self.fields['experiment_date'].widget = widgets.AdminDateWidget()
		#self.fields['project_name'].error_messages = {'required': 'FAS:DJFASKL:DJF'}
		
		#instance = getattr(self, 'instance', None)
		#if instance and instance.pk:
            	#	self.fields['experiment_id'].widget.attrs['readonly'] = True
	        	#self.fields['samples']=forms.ModelChoiceField(queryset=Experiment.objects.all())
	'''
	def clean_title(self):
		title = self.cleaned_data['title']
		if Experiment.objects.get(title=title).pk >0:
			raise ValidationError('ss')
			#raise ValidationError('This Experiment Title already exists! Please select a new name.')
		return title
	'''
	def clean_experiment_id(self):
		experiment_id = self.cleaned_data['experiment_id']
        	if experiment_id is None:
            		return self.fields['experiment_id'].initial
       		return experiment_id
	

	def clean(self):
        	cleaned_data = super(ExperimentForm, self).clean()
        	for key, value in cleaned_data.items():
            		if not value and key in self.initial:
                		cleaned_data[key] = self.initial[key]
        	return cleaned_data
	


class LogForm(forms.ModelForm):
	class Meta:
		model = Log
		exclude = ('related_exp','related_sam','created_by','created_date','updated_by','updated_date','download_by','download_date',)
	writer = selectable.AutoCompleteSelectMultipleField(
                lookup_class=InvestigatorLookup,
                label='Collaborators (Type to search)',
		required=False,
		)

class FinishForm(forms.ModelForm):
        class Meta:
                model = Experiment
		fields =('finish_flag','miseq_folder_name','analyst','comment')
	
	analyst = forms.ModelChoiceField(queryset=IDMSUser.objects.filter(role__iexact='analyst'),required=False)
	finish_flag = forms.ChoiceField(choices = (('Ongoing','Ongoing'),('Finished','Finished')), label="Experiment Status", widget=forms.Select(), required=True)


	

class SampleForm(forms.ModelForm):
	class Meta:
		model = Sample
		#fields=('index','cell_model','shRNA_library','shRNA_on','time_in_days','treatment','treatment_dose','replicate','other_tag','comment',)
        	exclude = ('experiment','feedback_flag','finish_flag','sample_name','created_by','created_date','updated_by','updated_date','download_by','download_date','sample_id','finish_flag',)
		labels = {
                  'treatment_dose': 'Treatment Dose (nM)',
                  'time_in_days': 'Time (Days)',
                  'shRNA_on': 'shRNA ON/OFF',
                  'pool_number': 'Pool Number',
		}
	#	widgets = {
	#	  'pool_number': forms.CheckboxSelectMultiple()
	#	}
		error_messages = {
                        'index': {'required': ("Required"),},
                        'cell_model': {'required':('Required'),},
                        'shRNA_library': {'required':('Required'),},
                        'shRNA_on': {'required':('Required'),},
                        'time_in_days': {'required':('Required'),},
                        'treatment': {'required':('Required'),},
                        'treatment_dose': {'required':('Required'),},
			'replicate': {'required':('Required'),},
		}
	

	cell_model = selectable.AutoCompleteSelectField(
        	lookup_class=CellmodelLookup,
       		label='Cell Model (Type to search)',
        	required=True,
		error_messages = {'required': ("Required"),},
    	)

    	shRNA_library = selectable.AutoCompleteSelectField(
        	lookup_class=ShrnaLookup,
        	label='shRNA Library (Type to search)',
        	required=True,
		error_messages = {'required': ("Required"),},
    	)

	def __init__(self, *args, **kwargs):
        	super(SampleForm, self).__init__(*args, **kwargs)
        	self.fields['shRNA_on'].required = True



        def clean(self):
		cleaned_data = super(SampleForm, self).clean()	
                
		index = cleaned_data.get('index')
                sample_name = cleaned_data.get('id')
		cell_model  = cleaned_data.get('cell_model')
		shRNA_library = cleaned_data.get('shRNA_library')
		time_in_days = cleaned_data.get('time_in_days')
		treatment = cleaned_data.get('treatment')
		treatment_dose = cleaned_data.get('treatment_dose')
		replicate = cleaned_data.get('replicate')
		pool_number = cleaned_data.get('pool_number')
		shRNA_on = cleaned_data.get('shRNA_on')
		other_tag = cleaned_data.get('other_tag')
		                

		if self.instance.experiment.sample_set.filter(cell_model=cell_model,shRNA_library=shRNA_library,time_in_days=time_in_days,treatment=treatment,treatment_dose=treatment_dose,shRNA_on=shRNA_on,other_tag=other_tag,replicate=replicate).count() > 0:
			
			raise ValidationError('Duplicated Sample Names! Change replicate if needed!')
		if self.instance.experiment.sample_set.exclude(sample_name=sample_name).filter(index=index).count() > 0:
                	#raise ValidationError(cleaned_data['id'])
                        raise ValidationError('This Index is already in use! Please select a different Index.')
                return cleaned_data


	#http://stackoverflow.com/questions/12905318/django-custom-form-validation-with-foreign-keys
        #def clean_index(self):
        #        index = self.cleaned_data['index']
	#	sample_name = self.data.get('id')
	#	if self.instance.experiment.sample_set.exclude(sample_name=sample_name).filter(index=index).count() > 0:
        #                raise ValidationError(sample_name)
			#raise ValidationError('This Index is already in use! Please select a different Index.')
        #        return index




SampleFormSet = inlineformset_factory(Experiment, Sample,
                                        form=SampleForm,
                                        #fields=('index','cell_model','shRNA_library','shRNA_on','time_in_days','treatment','treatment_dose','replicate','other_tag','comment',),
                                        #labels = {
                                        #'treatment_dose': 'Treatment Dose (nM)',
                                        #'time_in_days': 'Time (Days)',
                                        #'shRNA_on': 'shRNA ON/OFF',
                                        #},
                                        extra=1,
                                        can_delete = False,
                                        can_order = False
        )

SampleFormSet0 = inlineformset_factory(Experiment, Sample,
                                        form=SampleForm,
                                        extra=0,
                                        can_delete = False,
                                        can_order = False
        )


class SampleSheetImportForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    
