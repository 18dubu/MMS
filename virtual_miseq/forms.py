from django import forms
from models import Experiment, Sample
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets     
from django.core.exceptions import NON_FIELD_ERRORS
                                  
from parsley.decorators import parsleyfy

import selectable.forms as selectable
from .lookups import InvestigatorLookup,CellmodelLookup, ShrnaLookup




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
		exclude = ('experiment_id','feedback_flag','finish_flag','created_by','created_date','updated_by','updated_date','download_by','download_date','comment','design_type','finish_flag')
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
            		'project_name': {
                		'required': ("A project organizes related Experiments!"),
            		},
			'title': {'required':('How should I call you, my Experiment?'),},
			'description': {'required':('Some words for reference'),},
			'experiment_date': {'required':('Let\' make a schedule'),},
			'investigator': {'required':('Guy(s) who will conduct the experiment'),},
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

	#investigator  = make_ajax_field(Experiment, 'investigator', 'investigator', show_help_text=False)
	#investigator  = AutoCompleteSelectField( 'experiment', required=True, plugin_options = {'autoFocus': True, 'minLength': 4})	

	def __init__(self, *args, **kwargs):
        	#user = kwargs.pop('user','')
        	
		super(ExperimentForm, self).__init__(*args, **kwargs)
		#self.fields['experiment_date'].widget = widgets.AdminDateWidget()
		#self.fields['project_name'].error_messages = {'required': 'FAS:DJFASKL:DJF'}
		
		#instance = getattr(self, 'instance', None)
		#if instance and instance.pk:
            	#	self.fields['experiment_id'].widget.attrs['readonly'] = True
	        	#self.fields['samples']=forms.ModelChoiceField(queryset=Experiment.objects.all())

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
	


class SampleForm(forms.ModelForm):
	class Meta:
		model = Sample
		#fields=('index','cell_model','shRNA_library','shRNA_on','time_in_days','treatment','treatment_dose','replicate','other_tag','comment',)
        	exclude = ('feedback_flag','finish_flag','sample_name','created_by','created_date','updated_by','updated_date','download_by','download_date','sample_id','finish_flag',)
		labels = {
                  'treatment_dose': 'Treatment Dose (nM)',
                  'time_in_days': 'Time (Days)',
                  'shRNA_on': 'shRNA ON/OFF',
                  'pool_number': 'Pool Number',
		}
		#widgets = {
		#  'pool_number': forms.CheckboxSelectMultiple()
		#}
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
	
		#error_messages = {
                #        'index': {'required': ("What you can do without an unique Index"),},
                #        'cell_model': {'required':('Where does the cell come from?'),},
                #        'shRNA_library': {'required':('Where does the shRNA come from?'),},
                #        'shRNA_on': {'required':(''),},
		#	'time_in_days': {'required':('Time matters...'),},
		#	'treatment': {'required':('Pick one!'),},
		#	'treatment_dose': {'required':('It should be some integer in nM'),},
                #}


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


SampleFormSet = inlineformset_factory(Experiment, Sample,
                                        form=SampleForm,
                                        #fields=('index','cell_model','shRNA_library','shRNA_on','time_in_days','treatment','treatment_dose','replicate','other_tag','comment',),
                                        #labels = {
                                        #'treatment_dose': 'Treatment Dose (nM)',
                                        #'time_in_days': 'Time (Days)',
                                        #'shRNA_on': 'shRNA ON/OFF',
                                        #},
                                        extra=1,
                                        can_delete = True,
                                        can_order = False
        )

class SampleSheetImportForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

