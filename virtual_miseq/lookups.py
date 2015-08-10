from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from virtual_miseq.models import Experiment, Sample, Log, IDMSUser, MiseqIndex, CcleLibrary, ShrnaLibrary

from selectable.base import ModelLookup
from selectable.registry import registry

class InvestigatorLookup(ModelLookup):
    model = IDMSUser
    search_fields = ('FirstName__icontains', )
    def get_item_label(self, item):
    	return "%s %s (%s)" %(item.FirstName, item.LastName, item.EmailAddress)
registry.register(InvestigatorLookup)

'''
class InvestigatorLookup(LookupChannel):

    model = IDMSUser

    def get_query(self, q, request):
        return IDMSUser.objects.filter(Q(FirstName__icontains=q) |Q(LastName__icontains=q) | Q(EmailAddress__istartswith=q)|Q(NTID__icontains=q) ).order_by('LastName')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return escape(obj.FirstName) + ' ' + escape(obj.LastName)

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
	return u"%s<div><i>%s</i></div>" % (escape(obj.FirstName), escape(obj.email))

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
	return u"%s<div><i>%s</i></div>" % (escape(obj.FirstName), escape(obj.email))

class ExperimentLookup(LookupChannel):

    model = Experiment

    def get_query(self, q, request):
        return Experiment.objects.filter(title__icontains=q).order_by('-experiment_date')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.title

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div><i>%s</i></div>" % (escape(obj.title), escape(obj.experiment_id))
'''
class CellmodelLookup(ModelLookup):
    model = CcleLibrary
    search_fields = ('CCLE_name__icontains', )
registry.register(CellmodelLookup)

class ShrnaLookup(ModelLookup):
    model = ShrnaLibrary
    search_fields = ('LibName_Full__icontains', )
    def get_item_label(self, item):
        return "%s (%s)" %(item.LibName, item.LibName_Full)
registry.register(ShrnaLookup)

	
