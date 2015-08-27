

#Workflow to make changes to schema:
0. delete mis-configured table if needed (./manage.py dbshell DROP TABLE ~)
1. Use ./manage.py dbshell to empty the django_migrations table: delete from django_migrations; 
using: ./manage.py dbshell:DELETE FROM django_migrations WHERE app='my_app'
2. For every app, delete its migrations folder: rm -rf <app>/migrations/
3. Reset the migrations for the "built-in" apps: python manage.py migrate --fake
4. For each app run: python manage.py makemigrations <app>. Take care of dependencies (models with ForeignKey's should run after their parent model).
5. Finally: python manage.py migrate --fake-initial
After that I ran the last command without the --fake-initial flag, just to make sure.
Now everything works and I can use the migrations system normally.



#data import from IDMS
*Use the text format from MySQL as the source of import

##USER
Tested format: .txt/.csv
steps:
1. add column names to the first row
2. add an 'id' name with empty content in the following rows to the left of the first column
3.change the '\N' in the database to '' (empty cell)
4. Import



##cell models
1. add column names to the first row
2. add an 'id' name with empty content in the following rows to the left of the first column
3.change the name 'str' to 'str_mod'
4.!currently can not process date field, delete content of the date column
5.change the '\N' in the database to '' (empty cell)


##VectorLibrary
1. add column names to the first row
2. add an 'id' name with empty content in the following rows to the left of the first column
3.change the name 'type' to 'type_mod'; change the name "hash" to "hash_mod"
4.!currently can not process date field, delete content of the creation_date column
5.change the '\N' in the database to '' (empty cell)



##initial setup. Tested for fresh Ubuntu 14.04 install

apt-get install python-pip  # python-dev build-essential 
pip install --upgrade pip 
pip install django


pip install django-import_export
pip install django-ajax-selects
pip install django-selectable
pip install django-envelope
pip install django-  # pip install django==1.8.4

pip install django-crispy_forms
pip install django_datatables_view


#DB
apt-get install postgresql
apt-get install python-psycopg2

sudo su - postgres
createdb miseq_db
createuser mah29
psql
\password mah29
#type in password
\q  # quit psql

apt-get install python-ldap
apt-get install git
pip install git+https://github.com/pinax/django-mailer.git

./manage.py createsuperuser

#mail?
apt-get install postfix


#database upload
#upload from db/latest folders using admin site
#add analyst role to certain people from IDMS table
