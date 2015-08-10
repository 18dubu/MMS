from __future__ import unicode_literals

from django.contrib import admin
from .models import Experiment, Sample, Log, Treatment, IDMSUser, CcleLibrary, CellModel, VectorLibrary, ShrnaLibrary, MiseqIndex, PoolNumberChoice

from import_export.admin import ImportExportMixin, ExportActionModelAdmin

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

class SampleInline(admin.StackedInline):
    model = Sample

class ExperimentAdmin(ImportExportMixin, admin.ModelAdmin):
	list_filter = ['experiment_date','design_type','finish_flag','workflow', 'investigator']
	inlines = [
        	SampleInline,
    	]

class SampleAdmin(ImportExportMixin, admin.ModelAdmin):
    	list_filter = ['sample_name', 'experiment','time_in_days','created_by','shRNA_on','replicate']

class LogAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['writer', 'related_exp','related_sam','visible_to','created_by','updated_by','download_by']

class IDMSUserAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['Privilege', 'ValidationStatus','user_group','Shippingstate']
		
class CellModelAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['catalog_number', 'species','tissue','cell_type','disease','gender','validated','culture_medium','location']

class CcleLibraryAdmin(ImportExportMixin, admin.ModelAdmin):
	list_filter = ['Gender','Site_Primary','Hist_Subtype1','Source']

class VectorLibraryAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['vector_backbone', 'department','type_mod','promoter','gene','bacterial_selection','validations','protein','reporter']

class ShrnaLibraryAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['Source', 'Vector','Num_Pools','Num_shRNAs','Num_Genes','Num_shRNAsPerGene']

class MiseqIndexAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['index']

class TreatmentAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['Investigator','Source']
#class SampleAdmin(AjaxSelectAdmin):
#	form = make_ajax_form(Sample, {'experiment': 'experiment'})

class PoolNumberChoiceAdmin(ImportExportMixin, admin.ModelAdmin):
        list_filter = ['description']


admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(IDMSUser, IDMSUserAdmin)
admin.site.register(CcleLibrary, CcleLibraryAdmin)
admin.site.register(CellModel, CellModelAdmin)
admin.site.register(VectorLibrary, VectorLibraryAdmin)
admin.site.register(ShrnaLibrary, ShrnaLibraryAdmin)
admin.site.register(MiseqIndex, MiseqIndexAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(PoolNumberChoice, PoolNumberChoiceAdmin)
