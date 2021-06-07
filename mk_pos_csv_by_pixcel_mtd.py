import os
from glob import glob
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import shutil
import cv2
import numpy as np

# 이미지 디렉토리 읽어서, T-only 가져오고, 해당 포지션을 bed포맷으로 리턴

root_img_dir = r'E:/igv_img/SNP_Ter*/'
snapshot_path = r'for_detect_t_only_snapshots/*'
output_bed_dir = r'E:/igv_img/T-only_bedFiles/'

sample_dirs = glob(root_img_dir)
# print(sample_dirs)

for sample_dir in sample_dirs:
    # print("첫 루프")
    img_path_lst = glob(sample_dir + snapshot_path)
    # print(img_path_lst[0])
    sample_name = img_path_lst[0].split('\\')[1]
    print(sample_name)
    df_idx = 0

    bed_df = pd.DataFrame(columns=['CHROM', 'START', 'END'])

    for img_path in img_path_lst:
        # print("두번째 루프")
        # print(img_path)
        chr = img_path.split('\\')[-1].split(r'_')[0]
        start = img_path.split('\\')[-1].split(r'_')[1]
        end = img_path.split('\\')[-1].split(r'_')[2]
        # print(chr, '_', start, '_', end)

        src = cv2.imread(img_path, cv2.IMREAD_COLOR)
        # src = cv2.imread(img_path_lst[100], cv2.IMREAD_COLOR)
        # src[178, 800] = [0, 0, 0]

        # src[184, 800] = [0, 0, 0]

        # cv2.imshow("src", src)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # exit(0)

        if any(list(src[178, 800] - [202, 202, 202]) or any(list(src[178, 800] - [250, 250, 250]))): # 타겟 픽셀이 gray or white라면 (= t only) / 모두 0이어야 False반환. False일때 T-only
            if any(list(src[184, 800] - [202, 202, 202]) or any(list(src[184, 800] - [250, 250, 250]))): # 바로아래꺼 하나 더 검사
                continue
            else:
                bed_df.loc[df_idx] = [chr, start, end] # 딱 하나 있을때 T-only로 보자
                df_idx  = df_idx + 1

        else:
            bed_df.loc[df_idx] = [chr, start, end]
            df_idx  = df_idx + 1

            # print(bed_df)
            # print('회색 or 흰색이다')

        # exit(0)

    output_path = output_bed_dir + sample_name + '.bed'
    bed_df.to_csv(output_path, index=False, header=None, sep="\t")

        
        

exit(0)

# for i in range(len(input_lst)):
#     f_name = input_lst[i].split(r'/')[-1].split(r'.')[0].split(r'_')[-1]
#     csv_file = input_lst[i]
#     csv_df = pd.read_csv(csv_file, low_memory=False)
#     # print(csv_df)
#     bed_df = pd.DataFrame(columns=['CHROM', 'START', 'END', 'span'])
#     bed_df['CHROM'] = csv_df.pop('CHROM')
#     bed_df['START'] = csv_df.pop('POS')
#     bed_df['START'] = bed_df['START'] - 1
#     bed_df['span'] = csv_df.pop('ALT')
#     bed_df['span'] = bed_df['span'].map(len)
#     bed_df['END'] = bed_df['START'] + bed_df['span']
#     bed_df.pop('span')
#     # print(bed_df.head())

#     output_path = output_dir + prefix + f_name + '.bed'

#     bed_df.to_csv(output_path, index=False, header=None, sep="\t")





# path list 생성

img_path_lst = glob(origin_path)
# print(img_path_lst)
# exit(0)

label_dict = dict()

for path in img_path_lst:
    path_chunk = path.split('.')[0].split('\\')[-1]
    chr = path_chunk.split('_')[0]
    end = path_chunk.split('_')[2]
    key_tup = (chr, end)
    label_dict[key_tup] = path


# 라벨 불러와서 딕셔너리 화

label_df = pd.read_csv(root_img_dir + r'labelData.csv')
print(label_df)

# print(label_df.iloc[700])

# exit(0)



# i = label_df[(label_df["Comment"] == "LOW_DEPTH") | (label_df["Comment"] == "VARIANT_NOT_EXIST")].index
# print(i)
# label_df.drop(i, inplace=True)
# label_df.reset_index(drop=True, inplace=True)



# label_df = label_df[['chr', 'end', 'is_T_only_variant']]
# print(label_df)

print(label_df.shape)
print(range(label_df.shape[0]))



# y,x / b,g,r // [180, 810] = target point
# blue = [242  51  51]
# light green = [ 51 242  51]
# red = [ 51  51 242]
# brown = [ 55 136 208]
# gray = [202 202 202]

# print(label_dict)
# exit(0)

for idx in range(label_df.shape[0]):
    chr = label_df.loc[idx, 'chr']
    end = label_df.loc[idx, 'end']
    img_path = label_dict[(str(chr), str(end))]

    src = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # print("src[180, 710].all() =", src[180, 710].all())
    # print("np.array([202, 202, 202]) - np.array([202, 202, 202]) =", np.array([202, 202, 202]) - np.array([202, 202, 202]))
    # print("src[180, 710] - [202, 202, 202] =", src[180, 710] - [202, 202, 202])
    # print('type(list(src[180, 710] - [202, 202, 202]))', type(list(src[180, 710] - [202, 202, 202])))
    # print(any(list(src[180, 710] - [202, 202, 202]))) # false

    if any(list(src[180, 800] - [202, 202, 202]) or any(list(src[180, 800] - [250, 250, 250]))): # 타겟 픽셀이 gray or white라면 (= t only) / 모두 0이어야 False반환
        label_df.loc[idx, 'is_T_only_variant'] = 0
        # print('회색 or 흰색이 아니다')
    else:
        label_df.loc[idx, 'is_T_only_variant'] = 1
        # print('회색 or 흰색이다')
    # break
    # print(src[180, 800])
    # src[180, 800] = [0, 0, 0]

    # cv2.imshow("src", src)
    # # cv2.imshow("dst", dst)
    # cv2.imshow("add", add)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    

    # cv2.imwrite(copy_img_path, add)
    # break


# label_df.to_excel(root_dir + 'T6_only_check.xlsx')
label_df.to_csv(root_img_dir + 'T6_only_check2.csv')
