import pandas as pd
import os
from glob import glob
import shutil


# 엑셀에 필터된 데이터에 해당되는 igv 이미지 파일들을 서브셋

root_dir = r'D:/junmo/wd/WES/data/vcf/hard/WES1_210420/Teratoma_specifics/bed/T6I45/'
exel_file = r'SNP_Teratoma-6.xlsx'

input_img = r'snapshot_notsort_sqz_100/*'
output_dir = r'subset_img_t_only/'


img_path_lst = glob(root_dir + input_img)

label_dict = dict()

for path in img_path_lst:
    path_chunk = path.split('.')[0].split('\\')[-1]
    chr = path_chunk.split('_')[0]
    end = path_chunk.split('_')[2]
    key_tup = (chr, end)
    label_dict[key_tup] = path


label_df = pd.read_excel(root_dir + exel_file)

print(label_df)

label_df.dropna(inplace=True)

print(label_df)


i1 = label_df[label_df["is_T_only_variant"] != 1].index
label_df.drop(i1, inplace=True)
print(len(i1))


i2 = label_df[(label_df["Comment"] == "VARIANT_NOT_EXIST") | (label_df["Comment"] == "LOW_DEPTH")].index
label_df.drop(i2, inplace=True)
print(len(i2))


print(label_df)
label_df.reset_index(drop=False, inplace=True)

# print(label_dict)



for idx in range(label_df.shape[0]):
    chr = label_df.loc[idx, 'chr']
    end = label_df.loc[idx, 'end']
    img_path = label_dict[(str(chr), str(end))]
    # shutil.copy(img_path, root_dir + output_dir)




# 필터된 데이터에 clustered와 adjacent부분에 값을 넣어주기

# 후 - 전 == 1이면 전후 adj
# elif >= 15면 전후 clustered

for idx in range(label_df.shape[0] - 1):

    past_pos = label_df.loc[idx, 'end']
    post_pos = label_df.loc[idx + 1, 'end']
    gap = post_pos - past_pos
    if gap == 1:
        label_df.loc[idx, 'is_adjacent'] = 1
        label_df.loc[idx + 1, 'is_adjacent'] = 1
    elif gap <= 15:
        label_df.loc[idx, 'is_clustered'] = 1
        label_df.loc[idx + 1, 'is_clustered'] = 1


os.chdir(root_dir)

label_df.to_excel('processed_clust.xlsx')