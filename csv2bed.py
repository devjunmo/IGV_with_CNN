
# maf로 부터 chr start end만 엑셀로 가져와서 .bed로 만드는 코드

import os
import pandas as pd

root_path = r'E:/stemcell_ips/gdc/tech/29B/tech_comp/exclude_filterTag_tech_comp'
input_csv_name = r'hiPS29-B-tech_comp_specific_pos.csv'
output_bed_name = r'hiPS29-B-tech_comp_specific_pos.bed'

input_csv_path = os.path.join(root_path, input_csv_name)
output_bed_path = os.path.join(root_path, output_bed_name)

input_maf = pd.read_csv(input_csv_path, low_memory=False)

input_maf.to_csv(output_bed_path, sep='\t', index=False, header=False)