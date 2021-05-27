import os
from glob import glob
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import shutil
import cv2
import numpy as np


root_dir = r'D:/igv-deep/'
origin_path = root_dir + r'snapshots_ips_sample_1/*'

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

label_df = pd.read_csv(root_dir + r'labelData.csv')
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
label_df.to_csv(root_dir + 'T6_only_check2.csv')
