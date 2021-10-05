import os
import subprocess as sp
from glob import glob


# bed file로 부터 batch 스크립트 만들고, 
# 이미지 저장할 디렉토리도 동시에 생성

# SNP_로 시작하는 디렉토리들 가져오기
# 각 디렉토리 내부의 *.bed파일 가져오기\


root_dir = r'/myData/UTUC_WES/gdc/3rd/sub_case/127/'
bed_files = r'*.bed'
batch_output_dir_name = r'batch_files/'

snapshot_root_dir = root_dir + 'snapshots/'
b_script_img_output_root = r'E:\\IGV_DATA\\UTUC_WES\\gdc\\3rd\\sub_case\\127\\snapshots\\' # batch script에 넣을 문자열. 윈도우 IGV에서 읽을수 있어야 함
b_script_sfx = 'sp'

img_dir_name = 'specific_imgs'

batch_output_dir = root_dir + batch_output_dir_name

if os.path.isdir(snapshot_root_dir) is False:
    os.makedirs(snapshot_root_dir)

if os.path.isdir(batch_output_dir) is False:
    os.mkdir(batch_output_dir)


input_bed_lst = glob(root_dir + bed_files)


for i in range(len(input_bed_lst)):
    bed_path = input_bed_lst[i]
    bed_name = bed_path.split(r'/')[-1].split(r'.')[0].split(r'_')[0] # Teratoma-9
    var_type = bed_path.split(r'/')[-1].split(r'.')[0].split(r'_')[-2] # SNP
    output_path = batch_output_dir + var_type + '_' + bed_name + '_' + b_script_sfx + '.batch'

    b_script_img_dir = rf'{b_script_img_output_root}{bed_name}\\{img_dir_name}\\' # # batch script에 넣을 문자열
    img_dir = rf'{snapshot_root_dir}{bed_name}/{img_dir_name}'
    
    if os.path.isdir(img_dir) is False:
        os.makedirs(img_dir)

    sp.call(rf'bedtools igv -path {b_script_img_dir} -sort base -slop 50 -i {bed_path} > {output_path}', shell=True)




# for i in range(len(dir_lst)):
#     bed_path = os.path.join(root_dir, dir_lst[i])
#     output_path = os.path.join(root_dir, dir_lst[i], f'{dir_lst[i]}{batch_name}.batch')
#     # img_dir = os.path.join(root_dir, dir_lst[i], img_dir_name)
#     f_name = dir_lst[i].split('.')[0]
#     img_dir = rf'{img_output_root}{f_name}\\{img_dir_name}\\'
#     # print(img_dir)
#     if os.path.isdir(img_dir) is False:
#         os.mkdir(img_dir)
#     sp.call(rf'bedtools igv -path {img_dir} -sort base -slop 1 -i {bed_path} > {output_path}', shell=True)