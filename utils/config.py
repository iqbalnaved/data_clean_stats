#Configuration file - change values here
#path = '/home/purepredictive/clients/'
import os

#====General configuration====

##dir_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
##path = os.path.dirname(os.path.dirname(os.path.dirname(dir_path)))
##print dir_path
##print path
path = '/home/conveyor'

metafilename = 'metafile.inf'
metafieldSeparator = ' '

# final joined ppe file name
filename = 'joined.csv'
##filename = 'james_race.csv'
#filename  = "james_race"#
#filename = "james_race.csv"#
#filename = 'wgu_admissions_joined_csvs.csv'
#filename = 'choice_fall_joined_csvs.csv' #choice
#filename = 'rawcrest1.csv' #crest
#filename = 'full_data.csv'
#filename = 'bad_loansV1.csv'

#clientname = 'race'
clientname = 'testclient'
#clientname = 'jamesrace'
#clientname = 'wgu'
#clientname = 'wgu_small'
#clientname = 'choice'
#clientname = 'choice_small'
#clientname = 'crest'
#clientname = 'skullcandy'

#ensemble = 'gender' #race
ensemble = 'testensemble' #testclient
#ensemble = 'willfinish'#jamesrace
#ensemble = 'admissions' #wgu
#ensemble = 'oldfall' #choice
#ensemble = 'fall' #choice
#ensemble = 'fall' #choice
#ensemble = 'bad_loan' #crest
#ensemble = 'warranty' #skullcandy

'''
File naming convention:
1. Label files must have '_label' in their name
2. Subject files must have '_subject'
3. Topic ffies must have '_topic'
Each ensemble will have
1 label file
1 subject file
N topic files
'''

#testclient
fieldSeparator = { 'test_label.csv': ';'   ,
                   'test_subject.csv': ';' ,
                   'test_topic.csv': ','
                 }
               
##fieldSeparator = {'james_race2.csv': ','} # race

#choice
##fieldSeparator = {
##        'fall_claims_topic.csv': ',',
##        'fall_diagnostics_topic.csv': ',',
##        'fall_lab_topic.csv': ';',
##        'fall_patients_label.csv': ',',
##        'fall_rx_topic.csv': ';',
##        'fall_treatment_topic.csv': ',',
##        'patients_subject.csv': ','
##    }

#wgu 
##fieldSeparator = {
##        'lead_care_information_Topic.csv': ';',
##        'lead_care_status_Topic.csv': ';',
##        'lead_information_Subject.csv': ';',
##        'Lead_Label.csv': ',',
##        'lead_question_answers_Topic.csv': ';'
##
##    }

#skullcandy
##fieldSeparator = {
##        'coupon_visit_topic.csv': ';',
##        'orders_visit_topic.csv': ';',
##        'pageview_visit_topic.csv': ';',
##        'skullcandy_subject.csv': ';',
##        'tax_visit_topic.csv': ';',
##        'warranty_page_label.csv': ';'
##
##    }

extension = '.csv'

has_label = True #target concept boolean flag

key = 'StudentID'  # testclient
##key = 'PATIENT_ID' # choice
#key = 'LEAD_ID' # wgu
##key = 'VISIT_ID' # skullcandy

#paths

basePath = path + '/clients/' + clientname + '/ensembles/' + ensemble + '/input/data/'
print basePath

#====Scrubber configuration====
initial_null_limit_percent = 99
initial_upper_limit_abs = 50
initial_upper_limit_percent = 99
#numerical_upper_limit = 10000000
categorical_upper_limit_abs = 400 #use this...(8/2)
categorical_upper_limit_percent = 99

#====date formats=====

date_format_string = ['%Y/%m/%d','%Y-%m-%d'] # testensemble
#date_format_string = ['%m/%d/%y','%Y-%m-%d']  #James race
#date_format_string = ['%m/%d/%y','%Y-%m-%d','%m/%d/%y']  #James race
#date_format_string = ['%Y-%m-%d','%m/%d/%y','%m/%d/%y']  #James race
#date_format_string = ['%m/%d/%Y']  #wgu
#date_format_string = ['%Y-%m-%d %H:%M:%S']  #scala
#date_format_string = ['%m/%d/%y']  #progressive credit
#date_format_string = ['%m/%d/%Y', '%m/%d/%Y %H:%M:%S']#choice
#date_format_string = ['%m/%d/%y']#crest
#date_format_string = ['%Y-%m-%d %H:%M:%S'] #default
#date_format_string = ['%m/%d/%Y %H:%M:%S']#choice

#====override ====
numerical_override = []
categorical_override = []
date_override = []
geo_override = []
