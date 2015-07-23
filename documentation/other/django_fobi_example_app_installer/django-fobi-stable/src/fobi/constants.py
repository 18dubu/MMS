__title__ = 'fobi.constants'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'ACTION_CHOICE_REPLACE', 'ACTION_CHOICE_APPEND', 'ACTION_CHOICES',
    'CALLBACK_BEFORE_FORM_VALIDATION',
    'CALLBACK_FORM_VALID_BEFORE_SUBMIT_PLUGIN_FORM_DATA',
    'CALLBACK_FORM_VALID', 'CALLBACK_FORM_VALID_AFTER_FORM_HANDLERS',
    'CALLBACK_FORM_INVALID', 'CALLBACK_STAGES',
    'SUBMIT_VALUE_AS_VAL', 'SUBMIT_VALUE_AS_REPR', 'SUBMIT_VALUE_AS_MIX',
)

from django.utils.translation import ugettext_lazy as _

ACTION_CHOICE_REPLACE = '1'
ACTION_CHOICE_APPEND = '2'
ACTION_CHOICES = (
    (ACTION_CHOICE_APPEND, _("Append")),
    (ACTION_CHOICE_REPLACE, _("Replace")),
)

CALLBACK_BEFORE_FORM_VALIDATION = 'before_form_validation'
CALLBACK_FORM_VALID_BEFORE_SUBMIT_PLUGIN_FORM_DATA = 'before_submit_plugin_form_data'
CALLBACK_FORM_VALID = 'form_valid'
CALLBACK_FORM_VALID_AFTER_FORM_HANDLERS = 'after_form_handlers'
CALLBACK_FORM_INVALID = 'form_invalid'

CALLBACK_STAGES = (
    CALLBACK_BEFORE_FORM_VALIDATION,
    CALLBACK_FORM_VALID,
    CALLBACK_FORM_INVALID,
    CALLBACK_FORM_VALID_AFTER_FORM_HANDLERS,
)

SUBMIT_VALUE_AS_VAL = 'val'
SUBMIT_VALUE_AS_REPR = 'repr'
SUBMIT_VALUE_AS_MIX = 'mix'
