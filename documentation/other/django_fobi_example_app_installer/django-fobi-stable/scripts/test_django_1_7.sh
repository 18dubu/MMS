reset
./scripts/uninstall.sh
./scripts/install_django_1_7.sh
#cd ..
python examples/simple/manage.py test fobi --settings=settings_bootstrap3_theme_django_1_7 --traceback -v 3
#cd scripts