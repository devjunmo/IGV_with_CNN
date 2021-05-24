import os
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import shutil
import cv2


root_dir = r'D:/igv-deep/'
data_set_dir = root_dir + r'dataSet/'

# path list 생성

img_path_lst = glob(root_dir + r'snapshots_cnn_sort_1/*')
# print(img_path_lst[0])
# PIL.Image.open(str(img_path_lst[0])).show()

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

i = label_df[(label_df["Comment"] == "LOW_DEPTH") | (label_df["Comment"] == "VARIANT_NOT_EXIST")].index
print(i)
label_df.drop(i, inplace=True)
label_df.reset_index(drop=True, inplace=True)

label_df = label_df[['chr', 'end', 'is_T_only_variant']]
print(label_df)

print(label_df.shape)
print(range(label_df.shape[0]))

for idx in range(label_df.shape[0]):
    chr = label_df.loc[idx, 'chr']
    end = label_df.loc[idx, 'end']
    t_only = label_df.loc[idx, 'is_T_only_variant']
    img_path = label_dict[(str(chr), str(end))]
    img_path_name = img_path.split('\\')[-1]
    copy_img_path = ''

    if t_only == 0:
        # shutil.copy(img_path, data_set_dir + r'0/' + img_path_name)
        copy_img_path = data_set_dir + r'0/' + img_path_name
    elif t_only == 1:
        # shutil.copy(img_path, data_set_dir + r'1/' + img_path_name)
        copy_img_path = data_set_dir + r'1/' + img_path_name
    
    src = cv2.imread(img_path, cv2.IMREAD_COLOR)
    dst = src[170:1300, 800:825].copy()

    add = cv2.hconcat([dst, dst, dst, dst, dst, dst, dst, dst, \
                    dst, dst, dst, dst, dst, dst, dst, dst,])
    # dst = cv2.resize(dst, dsize=(22, 1830), interpolation=cv2.INTER_LINEAR)

    # cv2.imshow("src", src)
    # # cv2.imshow("dst", dst)
    # cv2.imshow("add", add)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # break

    cv2.imwrite(copy_img_path, add)
    # break

    
    


# 이미지 다듬기 
