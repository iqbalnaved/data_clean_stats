import numpy as np
import pandas as pd
#Create a dataframe for numerics

class Numeric_DataFrame:
	def __init__(self, df):
		self.df = df

	def create(self, num_list):
		df_numeric = pd.DataFrame(index=range(0,len(self.df.index)), columns=num_list, dtype=np.float) 
		for i in num_list:
			df_numeric[i] = self.df[i]
			del self.df[i]

		df_numeric.fillna(0,inplace=True)#fill nan with 0's
		return df_numeric