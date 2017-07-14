#date dateframe and transformation to timestamp
import pandas as pd
import numpy as np
from utils.column_typer import Typer
import calendar
import time
import datetime

class Date_Dataframe:
	def __init__(self, df):
		self.df = df
		self.ct = Typer(self.df)

	def create(self, date_list, date_format_list, persistent_index):
		df_date = pd.DataFrame(index=persistent_index, columns=date_list)
		for i in date_list:
                        #if i not a number, then convert. otherwise, leave it alone
			if type(self.df[i]) in self.ct.num_keys:
				df_date.update(self.df[i])
			else:
                                for date_format in date_format_list:
                                        date_temp = self.df[i].apply(lambda x: self.date_converter(x, date_format))
                                        if len(date_temp[date_temp == 253370764800L]) == 0: # no ValueError found
                                                break
				df_date.update(date_temp, overwrite = False)
				
		df_date.fillna(0,inplace=True)#replace nan with 0 value. This corresponds to 1/1/1970 Unix timestamp
		return df_date

	def date_converter(self, x, date_format):
		#if type(x) == str and np.isnan(x) == False:
                if type(x) == str and x != 'null':
##                        print 'x=' + x
##                        print 'date_format=' + date_format
                        
                        try:
                                y = calendar.timegm(time.strptime(str(x), date_format))
##                                print 'return=' + str(y)
                                return y
                        except ValueError:
##                                print 'ValeError'
                                return 253370764800L # timestamp for 1-1-9999

	def date_numeric(self, df, date_list, num_list):
		for i in date_list:
			if i in df.columns:
				num_list.append(i)
				date_list.remove(i)

	def date_format_finder(self, list):
		date_entries = []
		date_cols = list
		for i in list:
			date_entries.append(self.df[i][0])
		return zip(date_cols,date_entries)
