import numpy as np
import pandas as pd
from pandas import *
from operator import itemgetter
import logging
import math

class Categorical_DataFrame:
	def __init__(self, df):
		self.df = df
		self.cat_list_dict = {}

	def cat_list_dict_create(self, inlist):
		for i in inlist:
			self.df[i] = self.df[i].astype(object).replace(np.nan,'null') #key for making it run fast. Doesn't work well with nulls
			temp_set = self.df[i].unique()
			temp_set = list(temp_set)
			temp_set_dict = {}
			for k,v in enumerate(temp_set):
				temp_set_temp={v:k} #create value, index pair for everything in the set
				temp_set_temp['Unknown'] = k+1
				temp_set_dict.update(temp_set_temp)
			temp_dict = {i:temp_set_dict}
			self.cat_list_dict.update(temp_dict)#add logic for unknown variable + index
		return self.cat_list_dict

	def create(self, cat_list, persistent_index):
		self.cat_list_dict = self.cat_list_dict_create(cat_list)
		df_cat = pd.DataFrame(index = persistent_index, columns=cat_list)
		for i,j in enumerate(cat_list):
			print str(j) + ' ' + str(i) + ' out of ' + str(len(cat_list)) + ' categorical features mapped.'
			cat_list_dict_series = Series(self.cat_list_dict[j])
			cat_df_temp = self.df[j].map(cat_list_dict_series)
			#df_cat.insert(i, cat_df_temp, cat_df_temp.values)
			df_cat.update(cat_df_temp)
			df_cat = df_cat.T.groupby(level=0).first().T
		return df_cat

	def create_mrf(self, cat_list, cat_dict, persistent_index):
		df_cat = pd.DataFrame(index = persistent_index, columns=cat_list)
		logging.basicConfig(filename='badcat.log',level=logging.INFO)
		for i,j in enumerate(cat_list):
			self.df[j] = self.df[j].astype(object).replace(np.nan,'null')
			unique_vals = list(self.df[j].unique())#create a set from df[j] uniques
			not_in_trf = [x for x in set(unique_vals) if x not in set(cat_dict[j])]
			unique_vals[:] = ['Unknown' for x in unique_vals if x in not_in_trf]#replace items in unique_vals that are in not_in_trf
			print str(j) + ' ' + str(i) + ' out of ' + str(len(cat_list)) + ' categorical features mapped.'
			cat_list_dict_series = Series(cat_dict[j])
			unknown_dict = dict(zip(not_in_trf, unique_vals))
			print unknown_dict
			self.df[j].replace(to_replace = not_in_trf, value = unique_vals, inplace = True)
			cat_df_temp = self.df[j].map(cat_list_dict_series)
			df_cat.update(cat_df_temp)
			logging.info("Column: " + str(j) + str(not_in_trf) + "\n")
		return df_cat
