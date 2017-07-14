#Counts and reports features of initial dataframe. Output to a log file
import pandas as pd
import numpy as np

test_df = pd.DataFrame(np.random.randn(6,4))
print test_df
def count(df):
	intial_types = df.get_dtype_counts()
	
	for i in df.columns:
		unique_vals = df[i].unique()
		return len(unique_vals)
		break

print count(test_df)