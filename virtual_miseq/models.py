from django.db import models
import datetime
from django.utils import timezone
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
import uuid
import string
from django.utils import timezone
###############parameters######################

USER_PRIVILEGE_CHOICE=(('s','s'),('i','i'),('a','a'),('b','b'),('c','c'),('f','f'),('g','g'),('o','o'),('x','x'),('y','y'),('z','z'))

SAMPLE_REPLICATE_CHOICE = zip(list(string.ascii_uppercase),list(string.ascii_uppercase))

DISEASE_AREA_CHOICE = [('oncology','oncology')]

POOL_NUMBER_CHOICE = tuple([('None','None')]+zip([str(i) for i in range(1,7)], [str(i) for i in range(1,7)]))

##############Models###########################

class PoolNumberChoice(models.Model):
	description = models.CharField(max_length=300)

	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
                default=True
        )
	
	def __unicode__(self):
                return self.description


class MiseqIndex(models.Model):
	I7_Index_ID = models.CharField("I7 Index",max_length=32)
	index = models.CharField("MiSeq Index",max_length=32)

	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
                default=True
        )
	
	def as_json(self):
	        return dict(
        		id=self.id, 
			I7_Index_ID=self.I7_Index_ID,
            		index=self.index )

	def __unicode__(self):
                return str(self.I7_Index_ID +'-'+self.index)
	

class Treatment(models.Model):
        compoundName = models.CharField("Compound Name",max_length=64)
        CompoundFullName = models.CharField("CompoundFullName",max_length=256)
	PfizerNumber = models.CharField("Pfizer Number",max_length=32)
	Description = models.CharField("Description",max_length=256)
	Source = models.CharField("Source",max_length=256)
	Investigator = models.CharField("Investigator",max_length=32)

	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
                default=True
        )

        def __unicode__(self):
                return self.compoundName
	

class IDMSUser(models.Model):
        UserID = models.IntegerField("User ID",default=0)
        Username =  models.CharField("User Name",max_length=255,default='')
        Password =  models.CharField("Password",max_length=32,default='')
        EmailAddress =  models.EmailField("Email Address",max_length=255,default='')
        FirstName = models.CharField("First Name",max_length=65,default='')
        LastName = models.CharField("Last Name",max_length=65,default='')
        Phone = models.CharField("Phone",max_length=20,default='')
        Privilege = models.CharField("Privilege",
                                choices=USER_PRIVILEGE_CHOICE,
                                max_length=10,
                                default='c')
        ValidationStatus = models.CharField("Validation Status",max_length=30, default='pending')
        AuthenticationString = models.CharField("Authentication String",max_length=20,default='')
        user_group =  models.CharField("User Group",max_length=30,default='')
        Organization =  models.CharField("Organization",max_length=45,default='Oncology Research')
        Billingaddress =  models.CharField("Billing Address",max_length=150,null=True)
        Billingcity =  models.CharField("Billing City",max_length=100,null=True)
        Billingstate = models.CharField("Billing State",max_length=20,null=True)
        Billingzip = models.IntegerField("Billin ZIP",null=True)
        Shippingaddress = models.CharField("Shipping Adress",max_length=150,null=True)
        Shippingbuilding = models.CharField("Shipping Building",max_length=100,null=True)
        Shippingroom = models.CharField("Shipping Room",max_length=45,null=True)
        Shippingcity = models.CharField("Shipping City",max_length=100,null=True)
        Shippingstate =  models.CharField("Shipping State",max_length=20,null=True)
        Shippingzip = models.IntegerField("Shipping ZIP",null=True)
        NTID =  models.CharField("NTID",max_length=20,null=True)

	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
                default=True
        )

        def __unicode__(self):
                return str(self.FirstName +' '+self.LastName)
	
	@property
        def get_taged_investigator_name(self):
             	tags = "<span class=\'label label-info\' style=\'font-size:85%%;font-weight:500;background-color:#66C285;\'><a href=\'%s\'><font color='white'>%s</font></a></span>" % ('/virtual/search/?u='+'%20'.join([self.FirstName, self.LastName]), ' '.join([self.FirstName, self.LastName]))
                return tags



class CcleLibrary(models.Model):
	CCLE_name = models.CharField("CCLE Name",max_length=64,default='')
	Cell_line_primary_name = models.CharField("Cell Line Primary Name",max_length=150,null=True)
	Cell_line_aliases = models.CharField("Cell Line Aliases",max_length=150,null=True)
	#field added upon request by Jiyang, not existing in current import db
	Disease_Area =  models.CharField("Disease Area",max_length=150,null=True,default='Oncology')
	Gender = models.CharField("Gender",max_length=5,
		choices = (('M','M'),('F','F'),('U','U')),
		default = 'U'	
		)
	Site_Primary =  models.CharField("Site Primary",max_length=64,null=True)
	Histology =  models.CharField("Histology",max_length=64,null=True)
	Hist_Subtype1 =  models.CharField("Hist Subtype",max_length=64,null=True)
	Notes =  models.TextField('Note')
	Source = models.CharField("Source", max_length=32,null=True)
	
	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
                default=True
        )

	def __unicode__(self):

                return self.CCLE_name


class CellModel(models.Model):
	name = models.CharField("Name",max_length=150,null=True)
	parent = models.CharField("Parent",max_length=100,null=True)
	source = models.CharField("Source",max_length=45,null=True)
  	catalog_number = models.CharField("Catalog number",max_length=155,null=True)
  	species = models.CharField("Species",max_length=45,null=True)
  	ccle_name = models.CharField("Ccle name",max_length=100,null=True)
  	tissue = models.CharField("Tissue",max_length=100,null=True)
  	cell_type = models.CharField("Cell type",max_length=100,null=True)
  	disease = models.CharField("Disease",max_length=100,null=True)
   	histopath = models.CharField("Histopath",max_length=150,null=True)
  	gender = models.CharField("Gender",max_length=10,null=True)
  	engineering = models.CharField("Engineering",max_length=150,null=True)
  	selection = models.CharField("Selection",max_length=100,null=True)
  	validated = models.CharField("Validated",max_length=20,null=True)
  	str_mod =  models.TextField()
  	isoenzymes = models.CharField("Isoenzymes",max_length=45,null=True)
  	map_tested =  models.CharField("Map tested",max_length=45,null=True)
  	invivo_growth =  models.CharField("Invivo growth",max_length=45,null=True)
  	culture_medium =  models.CharField("Culture medium",max_length=155,null=True)
  	subculturing = models.TextField()
  	doubling =  models.CharField("Doubling",max_length=45,null=True)
  	commercial_link =  models.CharField("Commercial Link",max_length=255,null=True)
  	location =  models.CharField("Location",max_length=150,null=True)
  	submitter =  models.CharField("Submitter",max_length=100,null=True)
 	date = models.CharField('Date',max_length=45,null=True)#should be a DateField, check and change format later
  	comments =  models.TextField()
  	freezerpro_id = models.IntegerField("Freezerpro ID",null=True)

	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
                default=True
        )

	def __unicode__(self):

                return self.name

class VectorLibrary(models.Model):
  	name = models.CharField("Name",max_length=150,null=True)
  	shortname =  models.IntegerField("Short Name",null=True)
  	vector_backbone = models.CharField("Vector Backbone",max_length=150,null=True)
  	submitter = models.CharField("Submitter",max_length=45,null=True)
  	department = models.CharField("Department",max_length=100,null=True)
  	type_mod = models.CharField("Type",max_length=150,null=True)
  	application = models.CharField("application",max_length=150,null=True)
  	promoter = models.CharField("Promoter",max_length=150,null=True)
  	gene = models.CharField("Gene",max_length=150,null=True)
  	insert_origin = models.CharField("Insert origin",max_length=45,null=True)
  	bacterial_selection = models.CharField("Bacterial Selection",max_length=45,null=True)
  	other_selection = models.CharField("Other Selection",max_length=45,null=True)
  	reporter = models.CharField("Reporter",max_length=45,null=True)
  	dot_clone = models.CharField("Dot clone",max_length=45,null=True)
  	bacterial_stock = models.CharField("Bacterial stock",max_length=45,null=True)
  	bacterial_stock_type = models.CharField("Bacterial stock type",max_length=45,null=True)
  	bacterial_stock_location = models.TextField()
  	plasmid_dna_location = models.TextField()
  	plasmid_concentration = models.CharField('Plasmid concentration',max_length=45,null=True)#should be models.FloatField
  	vector_seq = models.TextField('Vector seq')
  	insert_seq = models.TextField('Insert seq')
  	upstream_atg = models.CharField("Upstream atg",max_length=45,null=True)
  	validations = models.TextField('Validations')
  	hash_mod = models.CharField("Hash",max_length=64,null=True)
  	creation_date = models.DateField('Creation date',null=True)
  	comments = models.TextField('Comments')
  	insert_accession = models.CharField("Insert accession",max_length=45,null=True)
  	transcript = models.TextField('Transcript')
  	protein = models.TextField('Protein')
  	orf = models.TextField('Orf')
	
	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
                default=True
        )	

	def __unicode__(self):

                return '-'.join([str(self.shortname),self.name])

class ShrnaLibrary(models.Model):
        LibName = models.CharField("Library Name",max_length=256,default='')
        LibName_Full = models.CharField("Library Full Name",max_length=256,default='')
        Description = models.TextField()
        Source = models.CharField("Source",max_length=256,default='')
        Vector = models.ForeignKey(VectorLibrary,blank=True,null=True,related_name='vector_shortname')
        Num_Pools = models.IntegerField("Number of Pools",null=True)
        CreationDate = models.CharField("Creation Date",max_length=256,null=True)
        Num_shRNAs = models.IntegerField("Number of shRNAs",null=True)
        Num_Genes = models.IntegerField("Number of genes",null=True)
        Num_shRNAsPerGene = models.IntegerField("Number of shRNAs per gene",null=True)
        AnnotationFile = models.CharField("Annotation File",max_length=512,default='')
        DNAStringSet_Object = models.CharField("DNAStringSet_Object",max_length=512,default='')
	
	approvalStatus = models.BooleanField(blank=True,
                choices = (
                        (True, "Approved"),
                        (False, "Pending")
                ),
		default=True
	)

        def __unicode__(self):
                return self.LibName

class Project(models.Model):
	name = models.CharField(max_length=200)
	
	#automatic-generated
        created_by = models.ForeignKey(IDMSUser,blank=True,null=True,related_name='pro_created_by')
        created_date = models.DateTimeField("Created Date",default=datetime.datetime.now,blank=True)
        updated_by = models.ManyToManyField(IDMSUser,blank=True,related_name='pro_updated_by')
        updated_date = models.DateTimeField("Updated date",auto_now_add=False, auto_now=True,blank=True,null=True)
        download_by = models.ManyToManyField(IDMSUser,blank=True,related_name='pro_download_by')
        download_date = models.DateTimeField("Download Date",null=True,blank=True)

        finish_flag = models.CharField(blank=True,max_length=20,
                        choices = (
                        ("Finished", "Finished"),
                        ("Ongoing", "Ongoing"),
                        ("Terminated","Terminated")
                ),
                default="Ongoing",
        )


	def __unicode__(self):
                return self.name


class Experiment(models.Model):
	#input-required
        experiment_id = models.CharField(max_length=200,blank=True, unique=True,default=uuid.uuid4)
	project_name =  models.CharField(max_length=200,default='')# models.ForeignKey(Project,related_name='experiments')#models.CharField(max_length=200,default='')
	title = models.CharField(max_length=200)
        description = models.TextField()
        experiment_date = models.DateTimeField('Date of experiment')
        investigator = models.ManyToManyField(IDMSUser,related_name='investigator')
	disease_area =  models.CharField("Disease Area",null=True,max_length=50,
					choices = DISEASE_AREA_CHOICE,
			                default = 'oncology'

	)
	workflow =  models.CharField(max_length=200,default='GenerateFASTQ')
	chemistry =  models.CharField(max_length=200,default='26DCx21x7')
	application =  models.CharField(max_length=200,default='FASTQ Only')
	assay =  models.CharField(max_length=200,default='TruSeq LT')
	version =  models.PositiveSmallIntegerField(default=4)
	reads =  models.BigIntegerField(default=21)
	#samples = models.TextField()
	#input-alternative
	design_type = models.CharField(max_length=200, null=True, blank=True)
	reverse_complement = models.IntegerField("Reverse Complement",default=0,null=True)
	feedback_flag =  models.CharField(blank=True,max_length=20,
                        choices = (
                        ("Negative", "Negative"),
                        ("Positive", "Positive"),
                        ("Questionable","Questionable")
                ),
                null=True,
        )

			#models.NullBooleanField(blank=True,null=True)
	comment =  models.CharField(max_length=200,blank=True,null=True)

	#automatic-generated
	created_by = models.ForeignKey(IDMSUser,blank=True,null=True,related_name='exp_created_by')
	created_date = models.DateTimeField("Created Date",default=timezone.now,blank=True)
	updated_by = models.ManyToManyField(IDMSUser,blank=True,related_name='exp_updated_by')
	updated_date = models.DateTimeField("Updated date",auto_now_add=False, auto_now=True,blank=True,null=True)
	download_by = models.ManyToManyField(IDMSUser,blank=True,related_name='exp_download_by')
	download_date = models.DateTimeField("Download Date",null=True,blank=True)

	finish_flag = models.CharField(blank=True,max_length=20,
                        choices = (
                        ("Finished", "Finished"),
                        ("Ongoing", "Ongoing"),
                        ("Terminated","Terminated")
                ),
		default="Ongoing",
        )


	def natural_key(self):
    		return (self.title,self.experiment_date)

	def created_within_one_week(self):
		return self.experiment_date >= timezone.now() - datetime.timedelta(days=7)

	def add_new_sample(self, new_sample):
		return self.sample_set.add(new_sample)
	
	def get_all_samples(self):
		return self.sample_set.all()
        @property
        def get_sorted_sample_set(self):
                return self.sample_set.order_by('created_date')

	@property
	def get_standard_created_date(self):
		#return "%s-%s-%s"%(self.created_date.year, self.created_date.month, self.created_date.day )
		return datetime.datetime(self.created_date.year, self.created_date.month, self.created_date.day,self.created_date.hour,self.created_date.minute,self.created_date.second).strftime("%Y-%m-%d %H:%M")

        @property
        def get_standard_experiment_date(self):
                return datetime.datetime(self.experiment_date.year, self.experiment_date.month, self.experiment_date.day).strftime("%Y-%m-%d ")


	@property
        def get_taged_project_name(self):
		return u"<span class=\'label label-info\' style=\'font-size:85%%;font-weight:500;background-color:#9999FF;\'><a href=\'%s\'><font color='white'>%s</font></a></span>" % ('/virtual/search/?p='+self.project_name.replace('\s+','%20'), self.project_name)


	@property
        def get_taged_investigator_name(self):
                tags = []
		for i in self.investigator.all():
			tags.append("<span class=\'label label-success\' style=\'font-size:85%%;font-weight:500;background-color:#66C285;\'><a href=\'%s\'><font color='white'>%s</font></a></span>" % ('/virtual/search/?u='+'%20'.join([i.FirstName, i.LastName]), ' '.join([i.FirstName, i.LastName])))
		
		return ', '.join(tags)

        @property
        def get_comma_separated_investigator_name(self):
                tags = []
                for i in self.investigator.all():
                        tags.append(' '.join([i.FirstName, i.LastName]))

                return ', '.join(tags)
	
	@property
        def get_taged_created_by_name(self):
                if self.created_by:
			tags="<span class=\'label label-success\' style=\'font-size:85%%;font-weight:500;background-color:#66C285;\'><a href=\'%s\'><font color='white'>%s</font></a></span>" % ('/virtual/search/?u='+'%20'.join([self.created_by.FirstName, self.created_by.LastName]), ' '.join([self.created_by.FirstName, self.created_by.LastName]))

                	return tags
		else:
			return ''


	@property	
	def get_absolute_url(self):
		return "/virtual/get/%s/" % self.experiment_id

        def __unicode__(self):
                return smart_unicode(self.title)

class Sample(models.Model):
	#user input
	index = models.ForeignKey(MiseqIndex, null=True,related_name='miseqIndex_index')
        sample_id =  models.IntegerField(blank=True,null=True)
	experiment = models.ForeignKey(Experiment,null=True,blank=True)

	cell_model = models.ForeignKey(CcleLibrary, null=True,related_name='cell_model')
	shRNA_library = models.ForeignKey(ShrnaLibrary, null=True,related_name='shRNA_LibName')
	pool_number = models.ManyToManyField(PoolNumberChoice,related_name='sample_pool_number',blank=True)
	shRNA_on = models.BooleanField(
		choices = (
    			(True, "ON"),
    			(False, "OFF")
		)
	)
	environment =  models.CharField(max_length=20,
                        choices = (
                        ("inVitro", "inVitro"),
                        ("inVivo", "inVivo"),
                ),
                default="inVitro",
        )

	replicate =  models.CharField(max_length=5,
                        choices = SAMPLE_REPLICATE_CHOICE,
                        null=True,
                        )

	time_in_days =  models.PositiveSmallIntegerField()
	treatment = models.ForeignKey(Treatment,blank=True, null=True,related_name='treatment_compoundName')
	treatment_dose = models.IntegerField(blank=True,null=True)
	feedback_flag = models.NullBooleanField(blank=True,null=True)
	finish_flag = models.CharField(blank=True,max_length=20,
			choices = (
                       	("Finished", "Finished"),
              		("Ongoing", "Ongoing"),
			("Terminated","Terminated")
                ),
		default="Ongoing",
	)
	other_tag =  models.CharField(max_length=200,blank=True,null=True)
	comment =  models.CharField(max_length=200,blank=True,null=True)
	
	# automatic generated
	sample_name = models.CharField(max_length=200,blank=True,null=True)  # generated by the syste

	#sample_creation_date =  models.DateTimeField(default=timezone.now, blank=True)
	
	created_by = models.ForeignKey(IDMSUser,blank=True,null=True,related_name='sample_created_by')
        created_date = models.DateTimeField("Created Date",default=datetime.datetime.now,blank=True)
        updated_by = models.ManyToManyField(IDMSUser,blank=True,related_name='sample_updated_by')
        updated_date = models.DateTimeField("Updated date",auto_now_add=False, auto_now=True,blank=True,null=True)
        download_by = models.ManyToManyField(IDMSUser,blank=True,related_name='sample_download_by')
        download_date = models.DateTimeField("Download Date",null=True,blank=True)

	@property
	def get_treatment_dosage_display(self):
		data = ''
		if self.treatment is not None:
			data = self.treatment.compoundName
		if self.treatment_dose is not None:
			data +=	' ('+str(self.treatment_dose)+' nM)'
		return data

	@property
        def get_pool_numbers_display(self):
                if self.pool_number is not None:
                        tmp=[]
			for pool in self.pool_number.all():
				tmp.append(pool.description)
			data = ','.join(tmp)
                return data



	def __unicode__(self):

                return unicode(self.sample_name)

'''
	@property	
	def generate_sample_name(self):
		
		
		#naming standard:
		#CellLine.Library.TreatmentIfAny.shON/shOFF.time.A/B/C
		#Example: A549.K1_2.EZH2_150nM.shON.T21.A
		
		treatment = '_'.join([self.treatment.compoundName,str(self.treatment_dose)])
		shrna = 'shON'
		if not self.shRNA_on:
			shrna = 'shOFF'
		
		self.sample_name = ".".join([self.cell_model.CCLE_name,treatment,shrna,''.join(['T',str(self.time_in_days)]), self.replicate])
	
		if self.other_tag:
			self.sample_name = self.sample_name + '.' + self.other_tag		
		return self.sample_name
'''
		
class Log(models.Model):
    writer = models.ManyToManyField(IDMSUser,related_name='writer',blank=True)
    subject = models.CharField(max_length=500)
    content = models.TextField()
    related_exp = models.ForeignKey(Experiment,blank=True,null=True,related_name='log_related_exp')
    related_sam = models.ForeignKey(Sample,blank=True,null=True,related_name='log_related_sam')
    visible_to =  models.CharField(blank=True,max_length=20,
                        choices = (
                        ("Everyone", "Everyone"),
                        ("Me", "Me"),
                        ("Collaborators","Collaborators")
                ),
                default="Collaborators",
        )

    created_by = models.ForeignKey(IDMSUser,blank=True,null=True,related_name='log_created_by')
    created_date = models.DateTimeField("Created Date",default=datetime.datetime.now,blank=True)
    updated_by = models.ManyToManyField(IDMSUser,blank=True,related_name='log_updated_by')
    updated_date = models.DateTimeField("Updated date",auto_now_add=False, auto_now=True,blank=True,null=True)
    download_by = models.ManyToManyField(IDMSUser,blank=True,related_name='log_download_by')
    download_date = models.DateTimeField("Download Date",null=True,blank=True)

    def __unicode__(self):
            return unicode(self.subject)




#############################Legacy Models############################


#Full IDMS cell model library, contain unnecessary information, mute for production and use new model: CellModelLibrary instead
'''
class CellModel(models.Model):
        #cell_line_name_short = models.CharField("Short Name",max_length=150,null=True)
        name = models.CharField("Name",max_length=150,null=True)
        parent = models.CharField("Parent",max_length=100,null=True)
        source = models.CharField("Source",max_length=45,null=True)
        catalog_number = models.CharField("Catalog number",max_length=155,null=True)
        species = models.CharField("Species",max_length=45,null=True)
        ccle_name = models.CharField("Ccle name",max_length=100,null=True)
        tissue = models.CharField("Tissue",max_length=100,null=True)
        cell_type = models.CharField("Cell type",max_length=100,null=True)
        disease = models.CharField("Disease",max_length=100,null=True)
        histopath = models.CharField("Histopath",max_length=150,null=True)
        gender = models.CharField("Gender",max_length=10,null=True)
        engineering = models.CharField("Engineering",max_length=150,null=True)
        selection = models.CharField("Selection",max_length=100,null=True)
        validated = models.CharField("Validated",max_length=20,null=True)
        str_mod =  models.TextField()
        isoenzymes = models.CharField("Isoenzymes",max_length=45,null=True)
        map_tested =  models.CharField("Map tested",max_length=45,null=True)
        invivo_growth =  models.CharField("Invivo growth",max_length=45,null=True)
        culture_medium =  models.CharField("Culture medium",max_length=155,null=True)
        subculturing = models.TextField()
        doubling =  models.CharField("Doubling",max_length=45,null=True)
        commercial_link =  models.CharField("Commercial Link",max_length=255,null=True)
        location =  models.CharField("Location",max_length=150,null=True)
        submitter =  models.CharField("Submitter",max_length=100,null=True)
        date = models.CharField('Date',max_length=45,null=True)#should be a DateField, check and change format later
        comments =  models.TextField()
        freezerpro_id = models.IntegerField("Freezerpro ID",null=True)

        def __unicode__(self):

                return self.name
'''

