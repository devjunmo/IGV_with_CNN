

import os
import subprocess as sp


# bed file로 부터 batch 스크립트 만들고, 
# 이미지 저장할 디렉토리도 동시에 생성

# SNP_로 시작하는 디렉토리들 가져오기
# 각 디렉토리 내부의 *.bed파일 가져오기\
# 

root_dir = r'/myData/WES/data/vcf/hard/WES1_210420/Teratoma_specifics/bed/'
img_output_root = r'E:\\igv_img\\'
batch_name = '_for_detect_t_only'
img_dir_name = 'for_detect_t_only_snapshots'

dir_lst = os.listdir(root_dir)

dir_lst = [item for item in dir_lst if 'SNP_' in item]

print(dir_lst)

for i in range(len(dir_lst)):
    bed_path = os.path.join(root_dir, dir_lst[i], f'{dir_lst[i]}.bed')
    output_path = os.path.join(root_dir, dir_lst[i], f'{dir_lst[i]}{batch_name}.batch')
    # img_dir = os.path.join(root_dir, dir_lst[i], img_dir_name)
    img_dir = rf'{img_output_root}{dir_lst[i]}\\{img_dir_name}\\'
    # print(img_dir)
    if os.path.isdir(img_dir) is False:
        os.mkdir(img_dir)
    sp.call(rf'bedtools igv -path {img_dir} -sort base -slop 1 -i {bed_path} > {output_path}', shell=True)