from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from forms import LoginForm
from virtual_miseq.models import IDMSUser

import sys
import ldap
import logging

logr = logging.getLogger(__name__)


#auth_view
def login(request):
    
    if request.POST:
	args = {}
        args.update(csrf(request))	
	#form = LoginForm(request.POST)
	if 1:#form.is_valid():
		has_error = False
		NTID = request.POST.get('username')#'mah29'
		passwd = request.POST.get('password')#'mhdPfizer1384'
	 	args['NTID'] = NTID	
		if not NTID:
			has_error = True
			args['ntid_error'] = 'NTID can not be empty'

		if not passwd:
                        has_error = True
                        args['passwd_error'] = 'Password can not be empty'


		Server = "ldap://amer.pfizer.com"
		un = 'amer\\'+ NTID
		l = ldap.initialize(Server)
		l.protocol_version = 3
		l.set_option(ldap.OPT_REFERRALS, 0)
		try:
			l.simple_bind_s(un, passwd)
		except ldap.INVALID_CREDENTIALS:
			has_error = True
			args['validate_error'] = 'Error validating NTID and password'		
		if has_error:
			return render(request,'login.html',args)	
		else:
			'''			
			baseDN = "OU=User, OU=Accounts, DC=amer.pfizer.com,DC=pfizer,DC=com"
			searchScope = ldap.SCOPE_SUBTREE
			retrieveAttributes = None 
			
			searchFilter = "(&(objectCategory=person)(objectClass=user)(sAMAccountName="+un+"))"#"cn=*"

			users = {}

			try:
				ldap_result_id = l.search(baseDN, searchScope, searchFilter)
				while 1:
				    rType, rData = l.result(ldap_result_id, 0)
				    if (rData == []):
					break
				    else:
					if rType == ldap.RES_SEARCH_ENTRY:
					    cn = rData[0][0]
					    data = rData[0][1]

					    #Flatten, just for more easy access
					    for (k, v) in data.items():
						if len(v) == 1:
						    data[k] = v[0]

					    uid = data["uid"]
					    users[cn] = data
				
			except ldap.LDAPError, e:
        			print e
    			finally:
        			l.unbind_s()
			'''
			#Check IDMS TABLE HAS THE CURRENT USER
			try:
				IDMS_user = IDMSUser.objects.get(NTID__iexact=NTID)
				email = IDMS_user.EmailAddress
			except IDMSUser.DoesNotExist:
				#add this user if not in IDMS TABLE, MAKE status to pending
				new_IDMS = IDMSUser(NTID=NTID,approvalStatus=False,FirstName=NTID,LastName=NTID,EmailAddress=NTID+"@PFIZER.COM")
				new_IDMS.save()
				email = ''
			#authenticate user
			user = auth.authenticate(username=NTID, password=NTID)
			if user is not None and user.is_active:
				auth.login(request, user)
			else:
				user = User.objects.create_user(NTID, email, NTID)
				user.save()
			return HttpResponse('<script type="text/javascript">if (window.opener){window.close();window.opener.location.href="/virtual/console/";}else{window.location.href="/virtual/console/";}</script>')
	
    else:
    	return render(request,'login.html')

    ''' 
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')
    '''
def loggedin(request):
    return render_to_response('loggedin.html', 
                              {'full_name': request.user.username})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/logout_success/")

def logout_success(request):
    return render_to_response('logout.html')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
        
    else:
        form = UserCreationForm()
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
    
    return render_to_response('register.html', args)



def register_success(request):
    return render_to_response('register_success.html')

def help(request):

    return render_to_response('help.html')

