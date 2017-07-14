#GOAL:
#FUTURE: Process all data in input?
import pandas as pd
from pandas import DataFrame
import csv
import os
import glob

class Formatter:
	def __init__(self):
		self = self

	'''def delimited2ppe(self, infileloc, metafilename, outfileLoc, metafieldSep):

		metafile = infileloc + metafilename
			df_meta  = pd.read_csv(metafile, sep= metafieldSep)

                for  i in range(0,len(df_meta.index)) : 
					filename = df_meta.iloc[i,0]
					fieldSeparator =df_meta.iloc[i,1]
					extension =df_meta.iloc[i,2] 
					infile = infileloc+filename+'.'+extension                   
                    
			#df = pd.read_csv(infile, warn_bad_lines = True, index_col = 0, header = 0, parse_dates = True, error_bad_lines = False, na_filter = False, nrows = 100) #Test. nrows = 10, will print out any lines with errors, but fails silently for these lines
			df = pd.read_csv(infile, sep=fieldSeparator, warn_bad_lines = True, index_col = 0, header = 0, parse_dates = True, error_bad_lines = False, na_filter = True) #Production.
			outfile = outfileLoc + filename + '.ppe'
		    df.to_csv(outfile, sep='\031')'''
	#Takes a file as input and return it in PPE format
	def delimited2ppe(self, infileloc, filename, outfileLoc, fieldSeperator):
		infile = infileloc + filename
		#df = pd.read_csv(infile, warn_bad_lines = True, index_col = 0, header = 0, parse_dates = True, error_bad_lines = False, na_filter = False, nrows = 100) #Test. nrows = 10, will print out any lines with errors, but fails silently for these lines
		df = pd.read_csv(infile, sep=fieldSeperator, warn_bad_lines = True, index_col = 0, header = 0, parse_dates = False, error_bad_lines = False, na_filter = True) #Production.
		outfile = outfileLoc + filename + '.ppe'
		df.to_csv(outfile, sep='\031')

	#Takes a group of files as input and converts to PPE format - BETA (7/23)
	def delimited2ppe_all(self, infileloc, filename, outfileLoc, fieldSeperator):
		file_list = glob.glob(infileloc + fieldSeperator)
		print file_list
		for i in file_list:
			print i
			filename = i.split('/')[-1]
			self.delimited2ppe(infileloc, filename, outfileLoc, fieldSeperator)

	#Initial dataframe formatting
	def initial_format(self, df):
		df = df.dropna(axis = 1, how = 'all')#remove blank columns
		df.rename(columns = lambda x: x.strip().replace(" ", "_"), inplace = True)#remove whitespace
		df.columns = [i.lower() for i in df.columns] #make column name in lower case
		return df

	#GOAL: Do an intial cardinality check for all columns to determine candidates for categorical type
	def categorical_checker(self,df):
		pass

class Output:
	def __init__(self):
		self.meta_final = ""
		self.meta_message = ""
		self.meta_numeric = []
		self.meta_numeric_index = []
		self.meta_cat =[]
		self.meta_cat_index = []
		self.meta_zip = []
		self.meta_zip_index = []

	#======= OUTPUT HEADERS TO CSV FILE ======
	def header_output(self, header, path):
		self.header_filename = path.split('.')[0] + '_header_index.csv'
		self.header_outfile = open(self.header_filename, "w")
		for i,j in enumerate(header):
			self.header_outfile.write(str(j) + ':' + str(i) + '\n')
		self.header_outfile.close()

	def header_output_comma(self, header, path):
		self.header_filename = path.split('.')[0] + '_header.csv'
		self.header_outfile = open(self.header_filename, "wb" )
		self.header_writer = csv.writer(self.header_outfile)
		self.header_writer.writerow(header)
		self.header_outfile.close()

	def meta_output(self, meta_message, path):
		self.meta_outfile = open(path, "w")
		self.meta_outfile.write(self.meta_message)
		self.meta_outfile.close()

	def cat_output(self, dictionary, path):
		self.meta_outfile = open(path, "w")
		self.meta_outfile.write(dictionary)
		self.meta_outfile.close()

	def geo_output(self, inputlist, path):
		self.meta_outfile = open(path, "w")
		self.meta_outfile.write(inputlist)
		self.meta_outfile.close()

	#CREATE META FILE
	def create(self, df_final, df_numeric, df_cat, df_zip):
		self.meta_count = len(df_final.columns) - 1 #do not need final label included

		#numerics
		for i,j in enumerate(df_numeric.columns):
			self.meta_numeric.append(j)
			#print self.meta_numeric
			self.meta_numeric_index.append(i)

		#categoricals
		for i in df_cat.columns:
			self.meta_cat.append(i)
		for i in range(len(self.meta_numeric_index),len(self.meta_cat) + len(self.meta_numeric_index)):
			self.meta_cat_index.append(i)  

		#geo
		for i in df_zip.columns:
			self.meta_zip.append(i)
		for i in range(len(self.meta_numeric_index) + len(self.meta_cat), len(self.meta_numeric_index) + len(self.meta_cat) + len(self.meta_zip)):
			self.meta_zip_index.append(i)
		
		self.meta_final = self.meta_numeric + self.meta_cat + self.meta_zip
		self.meta_message = 'features=' + str(self.meta_count) + '\n' + "numerical=" + ','.join(map(str,self.meta_numeric_index)) +  '\n' + "categorical=" + ','.join(map(str,self.meta_cat_index)) +  '\n' + "geo=" + ','.join(map(str,self.meta_zip_index))	

		#self.meta_message_features = "numerical=" + ',' + str(self.meta_numeric)
		self.meta_message_features = {'numerical':self.meta_numeric, 'categorical': self.meta_cat, 'geo' :self.meta_zip}
		return {'meta_message': self.meta_message, 'meta_final': self.meta_final, 'meta_final_features': self.meta_message_features}

