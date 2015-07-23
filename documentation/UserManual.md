MiSeq Management Syetem (MMS) rnai.pfizer.com User Manual

##NAME

MiSeq Management Syetem (MMS)

VERSION: 1.0

###DESCRIPTION
The MMS system, which is deployed to http://rnai.pfizer.com, aims to facilitate the automatic logging and management of MiSeq experiments for Pfizer researchers and managers.
The system enables the automatic generation of experiment plans (virtual MiSeq), the managemnet and update of existing ones. It also enables the general search and overview for all current experiment designs for managers. 


###ABOUT THIS VERSION
Version: 1.0 (alpha-release)
This is the first deployment of the system, general search, create new project and management functions are available. Feedbacks and function requests are gathered for future improvement.

##GETTING STARTED
*To use the system, visit http://rnai.pfizer.com (internal network)
*Only current Pfizer employee (with valid Pfizer network ID and password) can get the full functions of the application. Without login, one can search and use partial functions of the site.


###DIAGNOSTICS
1. If cannot connect to site, check whether your network if within Pfizer network or VPN status.
2. If cannot login to the system, check the correctness of your Pfizer ID and password.




##PROJECT STRUCTURE
###MODELS

The project was developed using Python 2.7 and django 1.8.
Dependencies include: django-csvimport, postgresql, 

1.virtual_miseq:
Current MiSeq experiment design (can be created by and logined user, might not be conducted yet)
Facilitate new experiment creation
Enable User login and user console for basic management

2.physical_miseq:
pool for all conducted experiments, for managers

3.admin
interface for system manager and developer


###VIEWS

###DATABASE

#Database import/export
Database can be import/export with Admin interface. 

####Export:
Click the export button on the upper right conor of each table (beside Add button). Different formats can be selected for exporting.

####Import:
File format including csv, xls, tsv, json, yaml are currently support for import function.
Please see the showing fields under "Import" label as a instrustion of what fields will be imported with current dta model.

NOTE THAT:
1. For current django-import-export module, the table for import must have a id column (also, the model one is uploading to must also have id as the primary key.) 
2.No special characters are currently allowed (ex: \N), please change them to allowed default value before import.

Resource:
https://github.com/django-import-export/django-import-export/issues/59
https://django-import-export.readthedocs.org/en/latest/import_workflow.html#import-data-method-workflow
https://github.com/django-import-export/django-import-export/issues/92


##AUTHOR

Jiyang Yu: Jiyang.yu2@pfizer.com
Handong Ma: handong.ma@pfizer.com



