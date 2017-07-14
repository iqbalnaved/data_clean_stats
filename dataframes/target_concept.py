#Create target concept from dataframe
# remove label column, which is assumed to be the last one by convention
import pandas as pd

class TargetConcept:
	def __init__(self, df):
		self.df = df
		self.target_list = []

	def target_concept(self, has_label):
		if has_label == True:
			target_concept = self.df[self.df.columns[len(self.df.columns) - 1]]
			df_target_concept = pd.DataFrame(target_concept)
			target_concept_header = self.df.columns[len(self.df.columns) - 1]
			self.df.pop(self.df.columns[len(self.df.columns) - 1]) #remove target concept from main data frame
		else:
			df_target_concept = pd.DataFrame(index=df.index, columns=range(0,1))
			df_numeric.fillna(0,inplace=True)#fill nan with 0's

		return df_target_concept.astype('int')

	def target_to_string(self, df):
		for i in df:
			self.target_list.append(i)
		self.target_list_to_str = ' '.join(target_list)
		return self.target_list_to_str

	def target_to_list(self, df):
		for i in df:
			self.target_list.append(i)
		return self.target_list
