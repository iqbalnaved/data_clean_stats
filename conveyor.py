#This is the main program that runs the conveyor. Will initially convert file to 
#ppe format, pivot/join, then convert to TRF format.

import pandas as pd
import numpy as np
import time
import datetime
import os
import math
import logging
import glob

from formatter.formatter import Formatter
from formatter.formatter import Output

from dataframes.target_concept import TargetConcept
from dataframes.df_numeric import Numeric_DataFrame
from dataframes.df_date import Date_Dataframe
from dataframes.df_categorical import Categorical_DataFrame
from dataframes.df_geo import Geo_DataFrame

from utils.scrubber import Scrubber
from utils.column_typer import Typer
from utils.pivoter import Pivoter
from utils.joiner import Joiner
import utils.config as config


#=====LOGGING======
logging.basicConfig(filename='info.log',level=logging.INFO)
start_time = time.time()
log_time = datetime.datetime.fromtimestamp(start_time).strftime('%m/%d/%Y %H:%M:%S')
logging.info('Started at: ' + str(log_time))

#========INPUTS INFO===========
path = config.path

date_format_string = config.date_format_string

filename = config.filename

#metafilename = config.metafilename
#metafieldSeparator = config.metafieldSeparator
logging.info('Filename: ' + str(filename))

clientname = config.clientname
ensemble = config.ensemble

fieldSeparator = config.fieldSeparator

extension = config.extension

basePath = config.basePath
ppePath = path + '/clients/' + clientname + '/ensembles/' + ensemble + '/results/data/'#ppe file to be used by Typer
ppeFinalFile = ppePath + filename + '.ppe'
outPath = path + '/clients/' + clientname + '/ensembles/' + ensemble + '/results/training/'
outFile = outPath + filename.split('.')[0]
metaFile = outPath + filename.split('.')[0] + '.meta'
metaFileFeatures = outPath + filename.split('.')[0] + '.features'
catFile = outPath + filename.split('.')[0] + '_cat.csv'
geoFile = outPath + filename.split('.')[0] + '_geo.csv'
dateFile = outPath + filename.split('.')[0] + '_date.csv'

#======DO NOT EDIT BELOW=============

#Convert the entire directory data to .ppe format. 
print 'Converting .csv files in the directory to .ppe format..'
format = Formatter()

os.chdir(basePath)
csv_list = []
for files in glob.glob("*.csv"):
    csv_list.append(files)

for csv in csv_list:
    print 'converting ' + csv
    print 'delim = ' + fieldSeparator[csv]
    if os.path.isfile(ppePath  + csv + '.ppe'): # remove older ones
        os.remove(ppePath  + csv + '.ppe')    
    format.delimited2ppe(basePath, csv, ppePath, fieldSeparator[csv])

# pivot the .ppe files in the directory
print 'pivot the .ppe files in the directory...'
pivoter = Pivoter()

os.chdir(ppePath)
ppe_list = []
for files in glob.glob("*.ppe"):
    ppe_list.append(files)

# if there is only 1 file then don't pivot, it's a subject file
if len(ppe_list) > 1: 
    for ppe in ppe_list:
        df = pd.read_csv(ppe, '\031')
        print 'pivoting ' + ppe
        pivot_type = pivoter.pivot(df, ppePath + '/' + ppe, '\031')
        if pivot_type > 0:
            os.remove(ppe)
    # recreate subject and label file by taking the only rows that 
    # has a instance key that exists in any of the pivoted files.
    print 'recreate subject and label file...'
    joiner = Joiner()
    joiner.adjust_subject_and_label_files(ppePath)

    # join the .ppe files and save
    print 'join the .ppe files and save...'
    joiner.join_ppe_files(ppePath, filename, config.key)
else:
    # only 1 file then don't pivot, it's a subject file
    # save subject file as ppe final file.
    df = pd.read_csv(ppe_list[0], '\031')
    df.to_csv(ppeFinalFile, sep='\031')
    
#load the single joined file (ppe format). Convert to dataframe
print 'loading ppe file..'
df = pd.read_csv(ppeFinalFile, sep = '\031')

#Initial Formatting
print 'Initial Formatting...'
df = format.initial_format(df)
#!!!! do initial scrubbing here as well

#Target Concept
print 'Extracting target concept..'
tc = TargetConcept(df)
df_target_concept = tc.target_concept(config.has_label)
print '\nTarget concept: ' + str(df_target_concept.columns)

#Null column scrubbing
print 'Scrubbing sparse features..'
scrubber = Scrubber(df)
scrubber.initial_nullscrubber_percent()
print '\nNull scrubbed features: ' + str(scrubber.scrubbed_list)

#column typing
print '\nLoad column typer keywords...'
ct = Typer(df)
master_list = ct.column_typer()
scrubber.remove(scrubber.scrubbed_list,master_list['cat_list'],master_list['num_list'],master_list['date_list'],master_list['zip_list'])
print '\nDates: ' + str(master_list['date_list'])
print '\nGeos: ' + str(master_list['zip_list'])
#Initial scrubbing
print 'Initial scrubbing...'
#scrubber.initial_scrubber_abs()
scrubber.initial_scrubber_percent() 
#print 'new df: ' + str(df)
print '\nInitial scrubbed features: ' + str(scrubber.scrubbed_list)

#output dates to file
date_output = ','.join(master_list['date_list'])
date_file = Output()
date_file.geo_output(date_output, dateFile)

scrubber.remove(scrubber.scrubbed_list,master_list['cat_list'],master_list['num_list'],master_list['date_list'],master_list['zip_list'])

#print df

#numerical
print 'numerical data typing and scrubbing'
df_numeric = Numeric_DataFrame(df)
if len(config.numerical_override) == 0:
    df_numeric_frame = df_numeric.create(master_list['num_list'])
else:
    df_numeric_frame = df_numeric.create(config.numerical_override)
print '\nNumerics: ' + str(df_numeric_frame.columns)

#categorical scrubbing/hashing

print '\nCategorical hashing'
print '\nCategoricals before scrubbing: ' + str(master_list['cat_list'])
#scrubber.categorical_scrubber_percent(df_cat_frame, master_list['cat_list'])
persistent_index = range(len(df.index))  # get number of rows for persistent index
#df = df.replace(np.nan,0) #!!!clean up null rows. May need to replace with something besides 0 - 6/26/13
scrubber.categorical_scrubber_abs(master_list['cat_list'])
print 'Categoricals after scrubbing: ' + str(master_list['cat_list'])

df_categorical = Categorical_DataFrame(df)
if len(config.categorical_override) == 0:
    df_cat_frame = df_categorical.create(master_list['cat_list'], persistent_index)
else:
    df_cat_frame = df_categorical.create(config.categorical_override, persistent_index)
#remove duplicate columns



print '\nCategoricals: ' + str(df_cat_frame)

#cat list output
cat_output = df_categorical.cat_list_dict_create(master_list['cat_list'])


#date transformation
df_date = Date_Dataframe(df)
print 'date transformation..'
print master_list['date_list']  #turn into date formatter
print '\nDate Formats. Please fix if necessary: ' + str(df_date.date_format_finder(master_list['date_list']))
#date_format = date_format_string*len(master_list['date_list'])
date_format = date_format_string

if len(master_list['date_list']) == 0:
    df_date_frame = pd.DataFrame(index = persistent_index)
elif len(config.date_override) == 0:
    df_date_frame = df_date.create(master_list['date_list'], date_format, persistent_index)
else:
    df_date_frame = df_date.create(config.date_override, date_format, persistent_index)
print '\nDate features: ' + str(df_date_frame.columns)
print 'df_date_frame='
print df_date_frame
df_numeric_frame = pd.concat([df_date_frame, df_numeric_frame], join = 'outer', axis = 1)
df_date.date_numeric(df_numeric_frame,master_list['num_list'], master_list['date_list'])


#geo transformation
print 'geo transformation..'
df_geo = Geo_DataFrame(df)
if len(config.geo_override) == 0:
    df_geo_frame = df_geo.create(master_list['zip_list'], 2)
else:
    df_geo_frame = df_geo.create(config.geo_override, 2)
print '\nGeo: ' + str(df_geo_frame.columns)

#merge dataframes
df_final = pd.concat([df_numeric_frame, df_cat_frame, df_geo_frame, df_target_concept], join = 'outer', axis = 1)
print df_final
df_mrf = pd.concat([df_numeric_frame, df_cat_frame, df_geo_frame], join = 'outer', axis = 1)
print 'Final length : ' + str(len(df_final))

#======= OUTPUT DATAFRAME TO TRF FILE =======
print '\nGenerating TRF File.....'

print 'OUTPUT DATAFRAME TO TRF FILE...'
outfile = outFile.split('.')[0] + '.trf' + extension
df_final.to_csv(outfile, header = False, index = False)

print '\nOUTPUT DATAFRAME TO MRF FILE...'
outfile_mrf = outFile.split('.')[0] + '.mrf' + extension
df_mrf.to_csv(outfile_mrf, header = False, index = False)

print '\nGenerating Meta File.....'
#==== META FILE===
print 'saving META FILE'
meta_file = Output()
meta_list = meta_file.create(df_final, df_numeric_frame, df_cat_frame, df_geo_frame)
meta_final = meta_list['meta_final']#header
meta_message = meta_list['meta_message']
meta_message_features = meta_list['meta_final_features']
#output_meta_header.meta_output(meta_message, metaFile)
meta_file.meta_output(meta_message, metaFile)
meta_file.cat_output(str(meta_message_features), metaFileFeatures)

print '\nGenerating Header File.....'
#==== HEADER FILE===
print 'saving HEADER FILE..'
target_list = tc.target_to_list(df_target_concept)
header = meta_final + target_list
meta_file.header_output(header, outFile)
meta_file.header_output_comma(header, outFile)

#output geos to file
zip_output = ','.join(master_list['zip_list'])
print zip_output
meta_file.geo_output(zip_output, geoFile)

#print '\nGenerating Categorical Hashing Record'
#output_meta_header.cat_output(df_categorical.cat_list_dict_create(df_cat_frame, list(df_cat_frame.columns)), catFile)

meta_file.cat_output(str(cat_output), catFile)
print '\nDONE.'
print 'Total time for job completion: ' + str(time.time() - start_time) + ' seconds.'

logging.info('Date Format: ' + str(date_format_string))
logging.info('Numerics: ' + str(master_list['num_list']))
logging.info('Categoricals: ' + str(master_list['cat_list']))
logging.info('Dates: ' + str(master_list['date_list']))
logging.info('Geo: ' + str(master_list['zip_list']))
logging.info('Scrubbed Features: ' + str(scrubber.scrubbed_list))
logging.info('Shape: ' + str(df_final.shape))
logging.info('Total time for job completion: ' + str(time.time() - start_time) + ' seconds.')

if __name__ == "__main__":
    import sys

