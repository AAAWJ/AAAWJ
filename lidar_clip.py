import shutil
import os
import xlwt
from tqdm import tqdm


def create_clip_sequence(lidar_folder_path):
    file_names_timestamp = os.listdir(lidar_folder_path)

    # 将文件名列表中时间戳转换为localtime
    lidar_time = [eval(timestamp.replace('.bin', '')[:10] + '.' + timestamp.replace('.bin', '')[10:]) for timestamp in
                  file_names_timestamp]
    lidar_time.sort()
    lidar_time = [format(item, '.6f') for item in lidar_time]

    clip_timestamp_xls = xlwt.Workbook()
    sh1 = clip_timestamp_xls.add_sheet('lidar_record')

    start_time_list = []
    end_time_list = []
    num = []

    i = 0
    pbar = tqdm(total=len(file_names_timestamp))  # 设置进度条总数

    while True:
        start_index = i
        start_time = float(lidar_time[i])
        seq = lidar_time[start_index:]
        end_time = start_time + 30
        diff = [abs(float(time) - end_time) for time in seq]
        diff_min = min(diff)
        end_index = diff.index(diff_min)
        if end_index == -1 or end_index == len(seq) - 1:
            clip_seq = seq
        else:
            clip_seq = seq[:end_index]
        start_time_list.append(clip_seq[0])
        end_time_list.append(clip_seq[-1])
        num.append(len(clip_seq))

        scene_path = os.path.join('G:/9.4clip_data/2023-09-04-13-47-56_1',
                                  clip_seq[0][:10] + clip_seq[0][11:])
        lidar_folder_path = os.path.join(scene_path, 'lidar')
        lidar_file_path = os.path.join(lidar_folder_path, 'lidar_top')

        os.makedirs(lidar_file_path, exist_ok=True)

        for k in clip_seq:
            file_name = k[:10] + k[11:] + '.bin'
            srcfile = os.path.join('F:/9.4_extract_rawdata/lidar_bin/2023-09-04-13-47-56_1', file_name)
            shutil.copy(srcfile, os.path.join(lidar_file_path, file_name))
            pbar.update(1)  # 更新进度条

        i = start_index + end_index

        if end_index == -1 or i >= len(lidar_time) - 1:
            break

    pbar.close()  # 关闭进度条

    # 写入起始时间和结束时间
    for i in range(len(start_time_list)):
        sh1.write(i, 0, start_time_list[i])
        sh1.write(i, 1, end_time_list[i])
        sh1.write(i, 2, num[i])
    clip_timestamp_xls.save(os.path.join('G:/9.4clip_data/2023-09-04-13-47-56_1', 'clip_timestamp.xls'))

    return num, file_names_timestamp


lidar_folder_path = r'F:\9.4_extract_rawdata\lidar_bin\2023-09-04-13-47-56_1'
num, file_names_timestamp = create_clip_sequence(lidar_folder_path)

# 核对总数
print(len(file_names_timestamp))
print(sum(num))
