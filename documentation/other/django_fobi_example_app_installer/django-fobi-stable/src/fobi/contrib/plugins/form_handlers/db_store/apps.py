__title__ = 'fobi.contrib.plugins.form_handlers.db_store.apps'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2014-2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Config',)

try:
    from django.apps import AppConfig

    class Config(AppConfig):
        name = 'fobi.contrib.plugins.form_handlers.db_store'
        label = 'fobi_contrib_plugins_form_handlers_db_store'

except ImportError:
    pass
