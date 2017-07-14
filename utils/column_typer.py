import pandas as pd
import numpy as np
import itertools
import os
#convert categoricals to date/geo and put in appropriate list

# first line date keywords
# second line zip keywords
# third line categorical keywords

class Typer:
	def __init__(self, df):
		__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		self.f = open(os.path.join(__location__, 'keywords.txt'));
		self.df = df
		self.keywords = [ map(str,line.strip().split(',')) for line in self.f ]
		self.num_keys = []
		self.date_list = []
		self.zip_list  = []
		self.cat_list  = []
		self.num_list  = []

	def column_typer(self):
		original_cols = sorted(list(self.df.columns))
		print 'original_cols: ' + str(original_cols)
		types = self.df.dtypes#Get data types of columns - check these
		typedict = types.to_dict()
		#mapping of type:column
		inv_map = {}
		for k, v in typedict.iteritems():
			inv_map[v] = inv_map.get(v, [])
			inv_map[v].append(k)

		#get object type columns
		object_dtypes = inv_map[np.dtype('object')] #this list is a numpy object type.
		object_dtypes = [i.lower() for i in object_dtypes]

		# get numeric columns
		for i in inv_map.keys():
			if i != 'object':
				self.num_keys.append(i)

		#append columns by type to numerical
		num_dtypes = []
		for i,j in enumerate(self.num_keys):
			num_dtypes.append(inv_map[self.num_keys[i]])

		#flatten the above list
		#numerical = [x for sublist in numerical for x in sublist] 
		num_dtypes = list(itertools.chain.from_iterable(num_dtypes))
		num_dtypes = [i.lower() for i in num_dtypes]

		'''date_list = []
		zip_list  = []
		cat_list  = []
		num_list  = []'''

		for k in range(0,len(self.keywords)):
			self.keywords[k] = [x.strip() for x in self.keywords[k]]    
			for i in original_cols[:]:
				for j in self.keywords[k]:
					if i.find(j) >= 0:
                                                print str(i) + ' has keyword ' + str(j)                                                
						if k == 0:                                                        
                                                        print str(i) + ' appended to date_list'
							self.date_list.append(i)# add as date column
						elif k == 1:
                                                        print str(i) + ' appended to zip_list'
							self.zip_list.append(i) # add as zip column
						elif k == 2:
                                                        print str(i) + ' appended to cat_list'
							self.cat_list.append(i) # add as categorical column
						elif k == 3:
							self.num_list.append(i)							
						try:
							original_cols.remove(i) # remove typed feature
						except ValueError:
							pass							
						try:
							object_dtypes.remove(i)
						except ValueError:
							pass
						try:
							num_dtypes.remove(i)
						except ValueError:
							pass

		# add rest of the object types as categoricals
		self.cat_list += object_dtypes
		
		# add rest of the num types as numerics
		self.num_list += num_dtypes

		return {'date_list': self.date_list, 'zip_list': self.zip_list, 'cat_list': self.cat_list, 'num_list': self.num_list}

	#detects numerical types
	def num_type(self):
		original_cols = list(self.df.columns)
		types = self.df.dtypes#Get data types of columns - check these
		typedict = types.to_dict()
		#mapping of type:column
		inv_map = {}
		for k, v in typedict.iteritems():
			inv_map[v] = inv_map.get(v, [])
			inv_map[v].append(k)

		#get object type columns
		object_dtypes = inv_map[np.dtype('object')] #this list is a numpy object type.
		object_dtypes = [i.lower() for i in object_dtypes]
		# get numeric columns
		
		for i in inv_map.keys():
			if i != 'object':
				self.num_keys.append(i)

		#print numerical_keys

		#append columns by type to numerical
		num_dtypes = []
		for i,j in enumerate(self.num_keys):
			num_dtypes.append(inv_map[self.num_keys[i]])

		#flatten the above list
		#numerical = [x for sublist in numerical for x in sublist] 
		num_dtypes = list(itertools.chain.from_iterable(num_dtypes))
		num_dtypes = [i.lower() for i in num_dtypes]
		
		return self.num_keys
