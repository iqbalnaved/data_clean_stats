# zip to geocode transformation
import pandas as pd
import numpy as np
from pyzipcode import ZipCodeDatabase
#import mapq
from pandas import *
import os


class Geo_DataFrame:
	'''
	lib_type = 0 pyzipcode 0.4
			   1 mapquest
			   2 GeoNames.org data
	'''
	def __init__(self, df):
		self.df = df
		self.lat_lng_cols = []

	def create(self, zip_list, lib_type = 0, api_key = 'Fmjtd%7Cluub2da2nu%2C8s%3Do5-9uand4'):

		# create lat and long column names from each zip column
		k = 0
		for z in zip_list:
			self.lat_lng_cols.append('Lat' + str(k))
			self.lat_lng_cols.append('Lng' + str(k))
			k += 1

		df_zip= pd.DataFrame(index=range(0,len(self.df.index)), columns=self.lat_lng_cols, dtype=np.float)
		
		#using pyzipcode 0.4 https://pypi.python.org/pypi/pyzipcode
		if (lib_type == 0):
			zcdb = ZipCodeDatabase()
			k = 0
			for i in zip_list:
				for j in range(0, len(self.df[i])):
					try:
						zipcode = zcdb[self.df[i][j]]
						df_zip[self.lat_lng_cols[k]][j] = zipcode.latitude
						df_zip[self.lat_lng_cols[k+1]][j] = zipcode.longitude
					except IndexError:
						pass
		elif lib_type == 1:
			# geocode conversion using mapquest api
			mapq.key(api_key)
			k = 0
			for n in zip_list:
				for i in range(0, len(self.df[n])):
					info = mapq.geocode(self.df[n][i])
					print str(info['adminArea1']) + ' ' + str(info['displayLatLng'])
					df_zip[k][i] = info['displayLatLng']['lat']
					df_zip[k+1][i] = info['displayLatLng']['lng']
				k += 2

		elif lib_type == 2:
			script_dir = os.path.dirname(__file__)
			rel_path = '../utils/allCountries_w_feature_names.txt'
			f = os.path.join(script_dir, rel_path)
			zipdb = pd.read_csv(f, sep='\t')
			zipdb = zipdb[(zipdb['country code']=='US') | (zipdb['country code']=='CA')] # take US & Canada for now.
			k = 0
			for n in zip_list:
				zipcode_list = self.df[n]
				zipcode_list = list(zipcode_list.T)
				lat_list = zipdb[zipdb['postal code'].isin(zipcode_list)]['latitude']
				lat_dict = dict(zip(zipdb['postal code'],zipdb['latitude']))
				lat_temp = self.df[n].map(lat_dict)
				df_zip[self.lat_lng_cols[k]] = lat_temp
				long_dict = dict(zip(zipdb['postal code'],zipdb['longitude']))
				long_temp = self.df[n].map(long_dict)
				df_zip[self.lat_lng_cols[k+1]] = long_temp
				k+=2

		#df_zip.fillna(0,inplace=True)#replace nan with 0 value.
		df_zip.fillna(0,inplace=True)
		return df_zip
