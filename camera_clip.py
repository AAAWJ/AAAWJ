import os
import shutil
import time
import xlrd
from xlutils.copy import copy
from numpy import size
import sys


'''
camera1:camera_left_front
camera2:camera_left_back
camera3:camera_right_back
camera4:camera_right_front
camera5:camera_front
camera7:camera_back
'''


def get_image_file_names(cameras_folder):
    """_summary_

    Args:
        cameras_folder (_type_): _description_

    Returns:
        _type_: _description_
    """
    image_file_names = []
    for i in range(len(cameras_flag)):
        per_camera_names_list = []
        for j in range(len(image_folder_per_cameras[i])):
            per_image_names_list = os.listdir(image_folder_per_cameras[i][j])
            per_image_names_list = [n[:16] for n in per_image_names_list]
            per_image_names_list = [n[:10] + '.' + n[10:] for n in per_image_names_list]
            per_image_names_list = [eval(n) for n in per_image_names_list]
            per_image_names_list.sort()
            per_image_names_list = [format(n, '.6f') for n in per_image_names_list]
            per_camera_names_list.append(per_image_names_list)
        image_file_names.append(per_camera_names_list)
    return image_file_names

def create_camera_image_folders(image_file_names, clip_start_timestamp_list, clip_end_timestamp_list, cameras_flag):
    """_summary_

    Args:
        image_file_names (_type_): _description_
        clip_start_timestamp_list (_type_): _description_
        clip_end_timestamp_list (_type_): _description_
        cameras_flag (_type_): _description_
    """
    for i in range(len(image_file_names)):
        m = 0
        num_all = size(image_file_names[i])
        num_check = []

        start_time_list = []
        end_time_list = []

        workbook = xlrd.open_workbook(os.path.join('G:/9.4clip_data/2023-09-04-13-47-56_1', 'clip_timestamp.xls'), formatting_info=True)
        new_workbook = copy(workbook)
        sh = new_workbook.add_sheet(cameras_flag[i])

        for j in range(len(clip_start_timestamp_list)):
            clip_start_time = clip_start_timestamp_list[j]
            clip_end_time = clip_end_timestamp_list[j]
            # 创建cameras文件夹及其子文件夹
            cameras_path = 'G:/9.4clip_data/2023-09-04-13-47-56_1/' + clip_start_time[:10] + clip_start_time[11:] + '/cameras'
            if not os.path.exists(cameras_path):
                os.mkdir(cameras_path)
            camera_path = cameras_path + '/' + cameras_flag[i]
            if not os.path.exists(camera_path):
                os.mkdir(camera_path)
            while True:
                camera_image_per_folder = image_file_names[i][m]
                # -1<时间-起始<0
                # 0<时间-终止<1
                # 起始<=time<=终止
                start = eval(clip_start_time) - 1
                end = eval(clip_end_time) + 1
                diff_start = [abs(eval(item) - start) for item in camera_image_per_folder]
                diff_end = [abs(eval(item) - end) for item in camera_image_per_folder]
                start_index = diff_start.index(min(diff_start))
                end_index = diff_end.index(min(diff_end))
                if end_index == -1 or end_index == len(camera_image_per_folder) - 1:
                    clip_seq = camera_image_per_folder[start_index:]  # 'XXXXXXXXXX.XXXXXX'
                else:
                    clip_seq = camera_image_per_folder[start_index: end_index + 1]
                start_time_list.append(clip_seq[0])
                end_time_list.append(clip_seq[-1])
                num_check.append(len(clip_seq))
                for n in clip_seq:
                    file_name = n[:10] + n[11:] + '.jpg'
                    srcfile = image_folder_per_cameras[i][m] + '\\' + file_name
                    shutil.copy(srcfile, camera_path + '/' + file_name)
                if (end_index == -1 or end_index == len(camera_image_per_folder) - 1) and min(diff_end) > 1:
                    m += 1
                else:
                    break
            # 显示进度条
            print("\r", end="")
            print("Progress: {}/{}  {}/{}: ".format(i + 1, len(image_file_names), j + 1, len(clip_start_timestamp_list)), "▋" * ((j + 1) // 2), end="")

        # 写入起始时间和结束时间
        for i in range(len(start_time_list)):
            sh.write(i, 0, start_time_list[i])
            sh.write(i, 1, end_time_list[i])
            sh.write(i, 2, num_check[i])
        new_workbook.save(os.path.join('G:/9.4clip_data/2023-09-04-13-47-56_1', 'clip_timestamp.xls'))

        # 核对数量
        print("\r", end="")
        print(num_all)
        print(sum(num_check))

        sys.stdout.flush()
        time.sleep(0.05)


cameras_folder = r'F:\9.4_extract_rawdata\camera'
cameras_flag = ['camera_left_front', 'camera_left_back', 'camera_right_back', 'camera_right_front', 'camera_front', 'camera_back']
camera_folder_names = os.listdir(cameras_folder) #相机文件名 列表[’camera1‘,'camera2',...]
image_folder_per_cameras = []
for i in range(len(camera_folder_names)):
    camera_folder_names[i] = cameras_folder + '\\' + camera_folder_names[i]
    per_cameras = os.listdir(camera_folder_names[i])
    for j in range(len(per_cameras)):
        per_cameras[j] = camera_folder_names[i] + '\\' + per_cameras[j]
    image_folder_per_cameras.append(per_cameras[2:4])

clip_lidar_timestamp_path = r'G:\9.4clip_data\2023-09-04-13-47-56_1\clip_timestamp.xls'
clip_timestamp = xlrd.open_workbook(clip_lidar_timestamp_path).sheets()[0]
clip_start_timestamp_list = clip_timestamp.col_values(0)
clip_end_timestamp_list = clip_timestamp.col_values(1)

image_file_names = get_image_file_names(cameras_folder)
create_camera_image_folders(image_file_names, clip_start_timestamp_list, clip_end_timestamp_list, cameras_flag)
