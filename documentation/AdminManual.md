

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





