
import pandas as pd
import numpy as np
import math
import os
import sys

class Pivoter:

    '''
    pivot type detection and execution
    '''    
    def pivot(self, df, infile, delim, architectural_limit = 50000):
            
        instance_key_column_num = 0
        topic_column_num = 1
        unique_topic_vals = set(df[df.columns[topic_column_num]])
        unique_topic_val_count = len(unique_topic_vals) # cardinality
        topic_attribute_count = len(df.columns) - 2 # omitting instance and topic key
        grouped = df.groupby(df.columns[instance_key_column_num])

        if grouped.size().max() > 1:

            if(topic_attribute_count == 0):
                sys.exit("Max group size > 1 but no topic attribute columns, remove duplicate instances.")
                
            topic_count_upper_limit = int(architectural_limit / topic_attribute_count )
            if unique_topic_val_count <= topic_count_upper_limit:
                print 'attempting pivot type 2'
                pivot_type=2
                df2 = self.type2(df)
            else:
                pivot_type=1
                # capping based on number of unique values in the topic column
                print 'attempting pivot type 1'
                diff = unique_topic_val_count - topic_count_upper_limit
                unique_topic_val_count -= diff
                unique_topic_val_count = 3
                df = self.cap_dataset(df, unique_topic_val_count)
                df2 = self.type1(df)

            # output to file
            filename_with_ext = os.path.basename(infile)
            basename = filename_with_ext.split('.')[0]
            path = os.path.dirname(infile);
            outfile = path + '/' + basename + '_pivot_' + str(pivot_type) +'.csv' # output csv file name
            if delim == '\031':
                outfile += '.ppe'
            df2.to_csv(outfile, header = True, index = True, sep = delim)
                
        else:
            pivot_type = 0
            print 'pivot 0: single instance per instance key.'

        return pivot_type

    '''
    unique_topic_val_count is used to take the intances with the most
    frequent topic values within unique_topic_value_count. This cut off is done
    to reduce feature numbers and thus decrease computational cost for the factory.
    '''

    def cap_dataset(self, df, unique_topic_val_count, instance_key_column_num=0, topic_column_num=1):
        unique_topic_vals = list(set(df[df.columns[topic_column_num]]))
        unique_topic_vals = unique_topic_vals[:unique_topic_val_count]
        # unique pivot values sorted by frequency from highest to lowest
        series = df.ix[:,topic_column_num].value_counts()
        unique_tv_sorted_by_freq = series.index # unique topic values sorted
        print unique_tv_sorted_by_freq
        unique_tv_sorted_by_freq = unique_tv_sorted_by_freq[:unique_topic_val_count] # cut off
        df_new = pd.DataFrame(columns = df.columns)            
        for tv in unique_tv_sorted_by_freq:
            df_filtered = df[df[df.columns[topic_column_num]] == str(tv)]        
            df_new = pd.concat([df_new, df_filtered])
        df_new.index = range(0,len(df_new))
        return df_new                    
        
    '''
    This function implements pivot Type 1:

    For each instance keys, there will be N number of rows ordered by datetime. The
    unique values in the topic column and the attribute columns in these N rows will
    create seperate columns. Therefore, for each unique instance key there will be a
    single record in the output csv file.

    If unique_topic_val_count > 0 it is used to take the intances with the most
    frequent topic values within unique_topic_value_count. This cut off is done
    to reduce feature numbers and thus decrease computational cost for the factory.

    '''

    def type1(self, df, instance_key_column_num=0, topic_column_num=1):

        topic_col_names = df.columns[topic_column_num:]
        
        unique_topic_vals = set(df[df.columns[topic_column_num]])        
        unique_topic_val_count = len(unique_topic_vals) # cardinality

        grouped = df.groupby(df.columns[instance_key_column_num])

        #create column names for df2
        new_col_names = []
        new_col_names.append(df.columns[instance_key_column_num])
        for g in range(1, grouped.size().max()+1):
            for i in range(0, len(topic_col_names)):
                new_col_names.append(topic_col_names[i] + str(g))

        # create df2
        df2 = pd.DataFrame(index=range(0,len(grouped)), columns=new_col_names)

        # get each group elements and create a single row from them
        for g in range(0,len(grouped)):
            print 'processing ' + str(g) + ' of ' + str(len(grouped))
            x = grouped.get_group(grouped.groups.keys()[g]) # get each group by key
            y = x.ix[:,1:] # exclude instance key column
            df2.iloc[g,0] = x.iloc[0,instance_key_column_num] # get instance key
            k = 1
            for i in range(0, len(y)):
                for j in range(0, len(y.iloc[0])):
                    df2.iloc[g,k] = y.iloc[i,j]            
                    k += 1
        
        df2.sort(df2.columns[instance_key_column_num],inplace=True)
        return df2


    '''
    This function implements pivot Type 2:

    DESCRIPTION:
    Determines unique topic values from the topic column. The number
    of topiced columns will be:

     no. of unique topic val * no of topic attributes.

    Popualate the new attribute columns by taking the corresponding values.

    Then aggregate (groupby) the columns according to unique instance
    key, topic key pair and take sum/max/min of the topic attribute values.

    '''    

    def type2(self, df, aggregate_func='max', instance_key_column_num = 0, topic_column_num = 1):

    ##  Causes ReshapeError for duplicate instance key and topic key pair
    ##    df2 = df.pivot(index=df.columns[instance_key_column_num],
    ##                   columns=df.columns[topic_column_num])
        
        grouped = df.groupby([df.columns[instance_key_column_num],df.columns[topic_column_num]])
        df = grouped.aggregate(getattr(np, aggregate_func))
        df = df.unstack()
    ##  df.columns = map(str.strip, map('_'.join, df.columns.values)) # join the tuples, srip() removes leading zeros and minus sign
        df.columns = map(lambda i: str(i[1]) + '_' + str(i[0]), df.columns.values) # convert tuple elements to string before joining
        return df
