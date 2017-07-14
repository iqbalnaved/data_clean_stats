#Scrubs a dataframe for cardincality
#=== SCRUB NUMERICS TO CATEGORICAL ===
import utils.config as config
from column_typer import Typer
import pandas as pd

class Scrubber:
	def __init__(self, df):
		self.df = df
		self.ct = Typer(self.df)
		self.scrubbed_list = []

	def initial_nullscrubber_percent(self):
		not_null_count = list(self.df.count()) #count() counts the not-null values
		i = 0
		for nnc in not_null_count:
                        print 'processing ' + str(i+1) + ' out of ' + str(len(self.df.columns))
			if ((len(self.df.index) - nnc)/float(len(self.df.index))) * 100 >= config.initial_null_limit_percent: # calculate null percentage
                                self.scrubbed_list.append(self.df.columns[i])
                                print 'scrubbed: ' + str(self.df.columns[i]) 				
                                del self.df[self.df.columns[i]]
                        else:        
                                i += 1

##		tf = pd.isnull(self.df) #convert to a boolean dataframe
##		k = 0
##		for i in tf.columns:
##			print i
##			true_tf = tf[tf[i] == 1][i] #nulls
##			#print true_tf
##			if (len(true_tf)/float(len(tf[i]))) * 100 >= config.initial_null_limit_percent:
##				self.scrubbed_list.append(i)
##				print 'scrubbed: ' + str(i) + ' iteration: ' + str(k)
##				del self.df[i]
##			k+=1


	def initial_scrubber_abs(self):
		master_list = self.ct.column_typer()
		num_types = self.ct.num_type()
		for i in self.df.columns:
			unique_vals = self.df[i].unique()
			#unique_vals = set(df[i])
			if len(unique_vals) >= config.initial_upper_limit_abs and type(self.df[i]) not in num_types and i not in master_list['date_list'] and i not in master_list['zip_list']: #adjust in config file
				self.scrubbed_list.append(i)
				del self.df[i]

	def initial_scrubber_percent(self):
		master_list = self.ct.column_typer()
		num_types = self.ct.num_type()
		for i in self.df.columns:
			#add check for mostly null column elements - reject if less than threshold
			#unique_vals = set(df[i])
			unique_vals = self.df[i].unique()
			if (len(unique_vals)/float(len(self.df[i])) * 100 >= config.initial_upper_limit_percent) and type(self.df[i]) not in num_types and i not in master_list['date_list']  and i not in master_list['zip_list']: #adjust in config file
				self.scrubbed_list.append(i)
				del self.df[i]

	def numerical_scrubber(self, df, num_list,cat_list):
		for i in num_list:
			#unique_vals = set(df[i])
			unique_vals = df[i].unique()
			if i in cat_list:
				if len(unique_vals) >= config.numerical_upper_limit or len(unique_vals <= 1): #adjust in config file
					self.scrubbed_list.append(i)
					cat_list.remove(i)
					del self.df[i]

	def categorical_scrubber_abs(self, cat_list):
		for i in cat_list:
			unique_vals = self.df[i].unique()
			if len(unique_vals) >= config.categorical_upper_limit_abs or len(unique_vals) <= 1: #adjust in config file
				cat_list.remove(i)
				self.scrubbed_list.append(i)
				del self.df[i]

	def categorical_scrubber_percent(self, cat_list):
		for i in cat_list:
			unique_vals = self.df[i].unique()
			if (len(unique_vals)/float(len(self.df[i])) * 100 >= config.categorical_upper_limit_percent) or len(unique_vals) <= 1: #adjust in config file
				cat_list.remove(i)
				self.scrubbed_list.append(i)
				del self.df[i]

	def remove(self, list0,list1,list2,list3,list4):
		for i in list0:
			if i in list1:
				list1.remove(i)
			elif i in list2:
				list2.remove(i)
			elif i in list3:
				list3.remove(i)
			elif i in list4:
				list4.remove(i)
