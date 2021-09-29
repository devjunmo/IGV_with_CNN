import io
import os
import pandas as pd
from glob  import glob
import os


input_dir = r'/myData/Teratoma_WGS/res_not_calling_WGS/'
input_format = r'*.csv'

input_res_lst = glob(input_dir + input_format)

header = ['CHR', 'START', 'END', 'RSLT']

out_df = pd.DataFrame(columns=['variant_exist', 'variant_not_exist', 'not_exist_%'])


for i in range(len(input_res_lst)):
    res = input_res_lst[i]

    sample_name = res.split(r'/')[-1].split(r'.')[0]

    res_df = pd.read_csv(res, names=header)
    
    # print(res_df)

    res_freq = pd.value_counts(res_df['RSLT'])

    # print(res_freq) # series

    v_exist = res_freq.loc['variant_exist']
    v_not_exist = res_freq.loc['variant_not_exist']
    
    per = round((v_not_exist / (v_not_exist + v_exist)) * 100, ndigits=2)

    out_df.loc[sample_name] = [v_exist, v_not_exist, per] 

    # res_df.loc[sample_name, 'variant_exist'] = v_exist
    # res_df.loc[sample_name, 'variant_not_exist'] = v_not_exist
    # res_df.loc[sample_name, 'not_exist_%'] = per


    # print(out_df)





    
    # break

out_df['variant_exist'] = out_df['variant_exist'].map(int)
out_df['variant_not_exist'] = out_df['variant_not_exist'].map(int)

print(out_df)