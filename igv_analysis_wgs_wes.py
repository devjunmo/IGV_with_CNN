
from class_IGV_snapshot_analysis import IgvSnapshotAnalysis


# def __init__(self, _snapshot_root_dir, _snapshots_dir_name, _save_to_result_dir):

snapshot_root_dir = r'/myData/Teratoma_WGS/snapshots/'
snapshots_dir_name = 'for_detect_not_calling_WGS'
save_to_result_dir = r'/myData/Teratoma_WGS/res_not_calling_WGS/'

isa = IgvSnapshotAnalysis(snapshot_root_dir, snapshots_dir_name, save_to_result_dir)

isa.start_analysis()

