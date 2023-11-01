import os
import shutil
import xlrd
import sys
import time
import xlwt
from xlutils.copy import copy

def get_radar_file_names(radar_folder_path):
    radar_file_names = []
    radar_folder_names = []
    radars_flag_old = os.listdir(radar_folder_path)
    for i in range(len(radars_flag_old)):
        radar_folder_names.append(os.path.join(radar_folder_path, radars_flag_old[i]))
        per_file_names = os.listdir(os.path.join(radar_folder_path, radars_flag_old[i]))
        per_file_names = [f[:16] for f in per_file_names]
        per_file_names = [eval(f[:10] + '.' + f[10:]) for f in per_file_names]
        per_file_names.sort()
        per_file_names = [format(item, '.6f') for item in per_file_names]
        radar_file_names.append(per_file_names)
    return radar_file_names, radar_folder_names

def create_radar_folders(radar_file_names, clip_start_timestamp_list, clip_end_timestamp_list, radars_flag):
    for i in range(len(radar_file_names)):
        num = len(radar_file_names[i])
        num_check = []

        start_time_list = []
        end_time_list = []

        workbook = xlrd.open_workbook(os.path.join('G:/9.4clip_data/2023-09-04-13-47-56_1', 'clip_timestamp.xls'),formatting_info=True)
        new_workbook = copy(workbook)
        sh = new_workbook.add_sheet(radars_flag[i])

        for j in range(len(clip_start_timestamp_list)):
            clip_start_time = clip_start_timestamp_list[j]
            clip_end_time = clip_end_timestamp_list[j]
            # 创建radars文件夹及其子文件夹
            radars_path = 'G:/9.4clip_data/2023-09-04-13-47-56_1/' + clip_start_time[:10] + clip_start_time[11:] + '/radars'
            if not os.path.exists(radars_path):
                os.mkdir(radars_path)
            radar_path = radars_path + '/' + radars_flag[i]
            if not os.path.exists(radar_path):
                os.mkdir(radar_path)
            data_per_radar = radar_file_names[i]
            # -1<时间-起始<0
            # 0<时间-终止<1
            # 起始<=time<=终止
            start = eval(clip_start_time) - 0.5
            end = eval(clip_end_time) + 0.5
            diff_start = [abs(eval(item) - start) for item in data_per_radar]
            diff_end = [abs(eval(item) - end) for item in data_per_radar]
            start_index = diff_start.index(min(diff_start))
            end_index = diff_end.index(min(diff_end))
            if end_index == -1 or end_index == len(data_per_radar) - 1:
                clip_seq = data_per_radar[start_index:]  # 'XXXXXXXXXX.XXXXXX'
            else:
                clip_seq = data_per_radar[start_index: end_index + 1]
            start_time_list.append(clip_seq[0])
            end_time_list.append(clip_seq[-1])
            num_check.append(len(clip_seq))
            for n in clip_seq:
                file_name = n[:10] + n[11:] + '.bin'
                srcfile = radar_folder_names[i] + '\\' + file_name
                shutil.copy(srcfile, radar_path + '/' + file_name)
            if end_index == -1 or end_index == len(data_per_radar) - 1:
                break
            # 显示进度条
            print("\r", end="")
            print("Progress: {}/{}  {}/{}: ".format(i + 1, len(radar_file_names), j + 1, len(clip_start_timestamp_list)), "▋" * ((j + 1) // 2), end="")

        # 写入起始时间和结束时间
        for k in range(len(start_time_list)):
            sh.write(k, 0, start_time_list[k])
            sh.write(k, 1, end_time_list[k])
            sh.write(k, 2, num_check[k])
        new_workbook.save(os.path.join('G:/9.4clip_data/2023-09-04-13-47-56_1', 'clip_timestamp.xls'))

        # 核对数量
        print("\r", end="")
        print(num)
        print(sum(num_check))

        sys.stdout.flush()
        time.sleep(0.05)

radar_folder_path = r'F:\9.4_extract_rawdata\radar_bin\2023-09-04-13-47-56_1'
radars_flag = ['radar_left_front', 'radar_front', 'radar_right_front', 'radar_left_back', 'radar_back', 'radar_right_back']

clip_lidar_timestamp_path = r'G:\9.4clip_data\2023-09-04-13-47-56_1\clip_timestamp.xls'
clip_timestamp = xlrd.open_workbook(clip_lidar_timestamp_path).sheets()[0]
clip_start_timestamp_list = clip_timestamp.col_values(0)
clip_end_timestamp_list = clip_timestamp.col_values(1)

radar_file_names, radar_folder_names = get_radar_file_names(radar_folder_path)
create_radar_folders(radar_file_names, clip_start_timestamp_list, clip_end_timestamp_list, radars_flag)
