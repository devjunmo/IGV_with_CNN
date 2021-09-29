# IGV_with_CNN

## 개발중

### class_IGV_snapshot_analysis.py 

pixcel_mtd를 클래스화 시킴

igv_analysis_wgs_wes.py에서 사용 예시 나옴


### pixcel_mtd.py

컬러에 특정 포지션을 찝어 픽셀 값을 가져옴
가져온 픽셀값에 대해 작업 수행


### mk_batch_file.py

igv용 batch파일 생성


### mk_pos_csv_by_pixcel_mtd.py

이미지를 읽어서 픽셀메소드 방식을 적용하여 T-only 포지션 구하고, 그걸 bed파일로 저장


### calc_result_freq.py

