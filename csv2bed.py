
# maf로 부터 chr start end만 엑셀로 가져와서 .bed로 만드는 코드

import os
import pandas as pd
import numpy as np
from glob import glob

# root_path = r'E:/UTUC_data/gdc_hg38/maf/2nd/DP_AF_filtered_maf/'
root_path = r'E:/UTUC_data/gdc_hg38/maf/5th/DP_AF_filtered_maf/exclude_filterTag_utuc'
input_csv_format = r'*.csv'

# output_bed_format = r'utuc_gdc-2nd-case5_pos.bed'

input_csv_path_lst = glob(os.path.join(root_path, input_csv_format))
# output_bed_path = os.path.join(root_path, output_bed_name)

for input_csv_path in input_csv_path_lst:

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

    f_name = os.path.split(input_csv_path)[1].split(r'.')[0]
    output_bed_name = f_name + r'.bed'

    output_bed_path = os.path.join(root_path, output_bed_name)

    input_maf.to_csv(output_bed_path, sep='\t', index=False, header=False)