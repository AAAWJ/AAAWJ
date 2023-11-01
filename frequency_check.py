import os
import sys
import time
import xlrd

'''
文件夹结构：
XXXXXXXXXXXXXX(scenes_file_name)
    -cameras
        -CAMERA_LEFT_FRONT
        -CAMERA_LEFT_REAR
        -CAMERA_RIGHT_REAR
        -CAMERA_RIGHT_FRONT
        -CAMERA_FRONT
        -CAMERA_REAR
    -lidar
        -LIDAR_TOP
    -radars
        -RADAR0
        -RADAR1
        -RADAR2
        -RADAR3
        -RADAR4
        -RADAR5
    -imu
'''

scenes_folder_path = r'F:\10.6示例数据\2023-09-03-14-57-42_1\clip_data' #切片后的文件夹
scenes_file_names = os.listdir(scenes_folder_path) #切片scenes的文件名列表 '...../XXXXXXXXXX'
#print(scenes_file_names)

sensor_folder_names = ['cameras', 'lidar', 'radars', 'imu']
cameras_folder_names = ['CAMERA_LEFT_FRONT',
                        'CAMERA_LEFT_REAR',
                        'CAMERA_RIGHT_REAR',
                        'CAMERA_RIGHT_FRONT',
                        'CAMERA_FRONT',
                        'CAMERA_REAR']
lidar_folder_names = ['LIDAR_TOP']
radars_folder_names = ['RADAR0',
                       'RADAR1',
                       'RADAR2',
                       'RADAR3',
                       'RADAR4',
                       'RADAR5']

clip_lidar_timestamp_path = r'F:\10.6示例数据\2023-09-03-14-57-42_1\clip_lidar_timestamp.xls'
clip_timestamp = xlrd.open_workbook(clip_lidar_timestamp_path).sheets()[0]
lidar_start_timestamp_list = clip_timestamp.col_values(0) #列表[‘XXXXX.bin’,...]
lidar_end_timestamp_list = clip_timestamp.col_values(1) #列表[‘XXXXX.bin’,...]
for i in range(len(lidar_start_timestamp_list)):
    start_time = lidar_start_timestamp_list[i].replace('.bin', '')
    end_time = lidar_end_timestamp_list[i].replace('.bin', '')
    lidar_start_timestamp_list[i] = start_time[:10] + '.' + start_time[10:] #列表['XXXXXX.XXXX']
    lidar_end_timestamp_list[i] = end_time[:10] + '.' + end_time[10:] #列表['XXXXXX.XXXX']

for i in range(len(scenes_file_names)):
    cameras_frequency = []
    radars_frequency = []
    lidar_frequency = []
    imu_frequency = []

    scene_path = scenes_folder_path + '\\' + scenes_file_names[i] #单一scenes文件夹路径
    #创建frequency文件
    frequency_file_path = scene_path + '\\frequency.txt'

    cameras_folder_path = scene_path + '\\' + sensor_folder_names[0]
    radars_folder_path = scene_path + '\\' + sensor_folder_names[2]
    lidar_folder_path = scene_path + '\\' + sensor_folder_names[1] + '\\' + lidar_folder_names[0]
    imu_file_path = scene_path + '\\' + 'imu.txt'

    lidar_time_interval = eval(lidar_end_timestamp_list[i]) - eval(lidar_start_timestamp_list[i])
    lidar_file_names = os.listdir(lidar_folder_path)
    lidar_num = len(lidar_file_names)
    lidar_frequency.append(str(lidar_num / lidar_time_interval))

    imu_time = []
    with open(imu_file_path, 'r', encoding='utf-8') as imu:
        for line in imu:
            data = line[:-1]  # 去掉换行符
            imu_time.append(eval(data.split(',')[0]))
    imu_time_interval = max(imu_time) - min(imu_time)
    imu_frequency.append(str(len(imu_time) / imu_time_interval))

    for m in range(len(cameras_folder_names)):
        camera_flag = cameras_folder_names[m]
        camera_file_path = cameras_folder_path + '\\' + camera_flag
        camera_file_names = os.listdir(camera_file_path)  # camera文件名 列表 ’XXXXXXXXX.jpg‘
        camera_time_interval_list = []
        for n in range(len(camera_file_names)):
            camera_time = camera_file_names[n][:16][:10] + '.' + camera_file_names[n][:16][10:]  # camera时间戳 'XXXXXX.XXX'
            camera_time_interval_list.append(eval(camera_time))
        camera_time_interval = max(camera_time_interval_list) - min(camera_time_interval_list)
        camera_frequency = len(camera_time_interval_list) / camera_time_interval
        cameras_frequency.append(str(camera_frequency))

    for m in range(len(radars_folder_names)):
        radar_flag = radars_folder_names[m]
        radar_file_path = radars_folder_path + '\\' + radar_flag
        radar_file_names = os.listdir(radar_file_path)  # camera文件名 列表 ’XXXXXXXXX.jpg‘
        radar_time_interval_list = []
        radar_frequency_list = []
        for n in range(len(radar_file_names)):
            radar_time = radar_file_names[n][:16][:10] + '.' + radar_file_names[n][:16][10:]  # radar时间戳 'XXXXXX.XXX'
            radar_time_interval_list.append(eval(radar_time))
        radar_time_interval = max(radar_time_interval_list) - min(radar_time_interval_list)
        radar_frequency = len(radar_time_interval_list) / radar_time_interval
        radars_frequency.append(str(radar_frequency))

    # 生成字典
    cameras_frequency_dict = dict(zip(cameras_folder_names, cameras_frequency))
    radars_frequency_dict = dict(zip(radars_folder_names, radars_frequency))
    lidar_dict = dict(zip(lidar_folder_names, lidar_frequency))
    imu_dict = dict(zip(imu_file_name, imu_frequency))
    scene_dict = {'lidar': lidar_dict, 'cameras': cameras_frequency_dict, 'radars': radars_frequency_dict, 'imu': imu_dict}

    with open(frequency_file_path, 'w', encoding='utf-8') as f:
        f.write('{\n')
        for item in scene_dict.items():
            f.write('\t' + item[0] + ':' + '{' + '\n')
            for k in item[1].items():
                f.write('\t' + '\t' + k[0] + ':' + k[1] + ',' + '\n')
            f.write('\t' + '}' + ',' + '\n')
        f.write('}')

    # 显示进度条
    print("\r", end="")
    print("Progress: {}/{}: ".format(i + 1, len(scenes_file_names)), "▋" * (i // 2), end="")
    sys.stdout.flush()
    time.sleep(0.05)