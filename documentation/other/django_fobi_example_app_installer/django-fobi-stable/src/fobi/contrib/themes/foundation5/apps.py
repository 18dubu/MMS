__title__ = 'fobi.contrib.themes.foundation5.apps'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Config',)

try:
    from django.apps import AppConfig

    class Config(AppConfig):
        name = 'fobi.contrib.themes.foundation5'
        label = 'fobi_contrib_themes_foundation5'

except ImportError:
    pass
