import pandas as pd
import numpy as np
import os
import glob

class Joiner:

    # recreate subject and label file by taking the only rows that 
    # has a instance key that exists in any of the pivoted files.
    def adjust_subject_and_label_files(self, ppePath, instance_key_column_num=0):

        ppe_list = []
        for files in glob.glob("*.ppe"):
            ppe_list.append(files)
        
        instance_key_list = []
           
        # read the pivot files and collect instance keys    
        for ppe in ppe_list:
            if '_topic' in ppe:
                df = pd.read_csv(ppePath + ppe, sep='\031')
                instance_key_list += list(df[df.columns[instance_key_column_num]])    
        # remove duplicate instance keys from list
        instance_key_list = list(set(instance_key_list))
        # filter subject and label file using the list
        for ppe in ppe_list:
            if '_subject' in ppe or '_label' in ppe:
                df = pd.read_csv(ppePath + ppe, sep='\031')
                df2 = df[df[df.columns[instance_key_column_num]].isin(instance_key_list)]
                if len(df2.index) < len(df.index): 
                    # save new subject and label file
                    df2.to_csv(ppePath + ppe, sep='\031')    

    # join the pivoted topic files with (adjusted) subject and label file
    def join_ppe_files(self, ppePath, ppe_final_filename, key):

        os.chdir(ppePath)
        ppe_list = []
        for files in glob.glob("*.ppe"):
            ppe_list.append(files)

        #rearrage file list so the label is joined last and subject file first
        for i in ppe_list:
            #determine label. move to end of the list    
            if '_label.' in i.lower():
                ppe_list.remove(i)
                ppe_list.insert(len(ppe_list),i)
            #determing subject. move to front of the list            
            if '_subject.' in i.lower():
                ppe_list.remove(i)
                ppe_list.insert(0,i)
                
        print ppe_list

        # read subject file   
        df_final = pd.read_csv(ppe_list[0], index_col=key, sep='\031')

        # add prefix to column names to avoid column overlapping
        prefix = 'sub.'
        new_col_names = []
        for col in df_final.columns:
            new_col_names.append(prefix + col)
        df_final.columns = new_col_names    

        df_index = df_final.index # for the subsequent files

        # read topic files
        i = 1
        for ppe in ppe_list[1:len(ppe_list)-1]:
            df = pd.read_csv(ppe, index_col=key, sep='\031')
            # add prefix to column names to avoid column overlapping
            prefix = 'tpc' + str(i) + '.'
            new_col_names = []
            for col in df.columns:
                new_col_names.append(prefix + col)
            df.columns = new_col_names
            df_final = df_final.join(df, on=df_index)
            del df
            i += 1

        # read label file
        df = pd.read_csv(ppe_list[len(ppe_list)-1], index_col=key, sep='\031')

        # add prefix to column names to avoid column overlapping
        prefix = 'lbl.'
        new_col_names = []
        for col in df.columns:
            new_col_names.append(prefix + col)
        df.columns = new_col_names    

        df_final = df_final.join(df, on=df_index)
        del df

        df_final = df_final.dropna(axis = 1, how = 'all')#remove blank columns
       
        df_final.to_csv(ppePath + ppe_final_filename +'.ppe', sep='\031')#output file    
