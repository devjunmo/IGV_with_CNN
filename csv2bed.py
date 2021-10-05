
# maf로 부터 chr start end만 엑셀로 가져와서 .bed로 만드는 코드

import os
import pandas as pd
import numpy as np

root_path = r'E:/UTUC_data/gdc_hg38/maf/3rd/DP_AF_filtered_maf/sub_pos/'
input_csv_name = r'case127_pos.csv'
output_bed_name = r'utuc_3rd-case127_pos.bed'

input_csv_path = os.path.join(root_path, input_csv_name)
output_bed_path = os.path.join(root_path, output_bed_name)

input_maf = pd.read_csv(input_csv_path, low_memory=False)

# print(input_maf)
print(input_maf.shape)
print(input_maf.dtypes)

input_maf.dropna(inplace=True)

input_maf['Start'] = input_maf['Start'].apply(np.int)
input_maf['End'] = input_maf['End'].apply(np.int)

# print(input_maf)
print(input_maf.shape)
print(input_maf.dtypes)

input_maf.to_csv(output_bed_path, sep='\t', index=False, header=False)