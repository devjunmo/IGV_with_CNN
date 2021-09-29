import pandas as pd
import cv2
import os
from glob import glob

# 디렉토리 구조

# snapshot_root/ ---- Sample1/ - snapshotsDir/ - images ...
#        |
#        ------------ Sample2/ - snapshotsDir/ - images ...
#        |      ...
#        :



class IgvSnapshotAnalysis():

    def __init__(self, _snapshot_root_dir, _snapshots_dir_name, _save_to_result_dir):
        self.sample_dirs = glob(_snapshot_root_dir + '*')
        self.snapshots_dir_name = _snapshots_dir_name # ex) for_detect_t_only_snapshots
        self.save_to_result_dir = _save_to_result_dir

        IgvSnapshotAnalysis.__mk_dir(self.save_to_result_dir)

    
    @classmethod
    def __mk_dir(cls, _dir):
        if os.path.isdir(_dir) is False:
            os.mkdir(_dir)


    def start_analysis(self):
        for sample_dir in self.sample_dirs:
            # print(sample_dir)
            # print(self.snapshots_dir_name)
            # print(sample_dir + r'/' + self.snapshots_dir_name + r'/*')
            img_path_lst = glob(sample_dir + r'/' + self.snapshots_dir_name + r'/*')
            # print(img_path_lst)

            if not img_path_lst:
                continue

            sample_name = img_path_lst[0].split(r'/')[-3]
            print(sample_name)
            df_idx = 0
            res_df = pd.DataFrame(columns=['CHROM', 'START', 'END', 'RSLT'])

            for img_path in img_path_lst:
                chr = img_path.split(r'/')[-1].split(r'_')[0]
                start = img_path.split(r'/')[-1].split(r'_')[1]
                end = img_path.split(r'/')[-1].split(r'_')[2]
                # print(chr, '_', start, '_', end)

                src = cv2.imread(img_path, cv2.IMREAD_COLOR)
                # src = cv2.imread(img_path_lst[100], cv2.IMREAD_COLOR) # GUI 환경에서 디버깅 가능
                # src[178, 800] = [0, 0, 0]

                # src[184, 800] = [0, 0, 0]

                # cv2.imshow("src", src)
                # cv2.waitKey()
                # cv2.destroyAllWindows()
                # exit(0)


                # 타겟 픽셀이 gray or white라면 (= variant not exist, 0) / 모두 0이어야 False반환. False일때 variant not exist, 0
                if any(list(src[178, 800] - [202, 202, 202]) or any(list(src[178, 800] - [250, 250, 250]))): 

                    if any(list(src[184, 800] - [202, 202, 202]) or any(list(src[184, 800] - [250, 250, 250]))): # 바로아래꺼 하나 더 검사
                        res_df.loc[df_idx] = [chr, start, end, 'variant_exist']
                        df_idx  = df_idx + 1
                    else:
                        res_df.loc[df_idx] = [chr, start, end, 'variant_not_exist'] # 딱 하나 있을때 variant not exist로 보자
                        df_idx  = df_idx + 1

                else:
                    res_df.loc[df_idx] = [chr, start, end, 'variant_not_exist']
                    df_idx  = df_idx + 1

                    # print(bed_df)
                    # print('회색 or 흰색이다')

                # exit(0)

            output_path = self.save_to_result_dir + sample_name + '.csv'
            res_df.to_csv(output_path, index=False, header=None)



    

