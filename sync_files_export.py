import json
import os
import shutil
import sys
import time
import shutil
import json

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
        -RADAR_LEFT_FRONT
        -RADAR_FRONT
        -RADAR_RIGHT_FRONT
        -RADAR_LEFT_REAR
        -RADAR_REAR
        -RADAR_RIGHT_REAR
'''

'''
创建字典
dic = dict(zip('abc', [1, 2, 3]))
print(dic)
# 输出结果：{'a': 1, 'b': 2, 'c': 3}
'''

scenes_folder_path = r'G:\9.4clip_data\2023-09-04-13-47-56_1' #切片后的文件夹
scenes_file_names = os.listdir(scenes_folder_path)[:10] #切片scenes的文件名列表 '...../XXXXXXXXXX'
#print(scenes_file_names)

sensor_folder_names = ['cameras', 'lidar', 'radars']
cameras_folder_names = ['camera_left_front',
                        'camera_left_back',
                        'camera_right_back',
                        'camera_right_front',
                        'camera_front',
                        'camera_back']
lidar_folder_names = ['lidar_top']
radars_folder_names = ['radar_left_front',
                       'radar_front',
                       'radar_right_front',
                       'radar_left_back',
                       'radar_back',
                       'radar_right_back']

for i in range(len(scenes_file_names)):
    # 相机和雷达最近帧 和folder_names一一对应
    lidar = []
    cameras_nearest = []
    radars_nearest = []

    scene_path = scenes_folder_path + '\\' + scenes_file_names[i] #单一scenes文件夹路径
    #创建sync_file路径
    sync_folder_path = scene_path + '\\sync_files'
    if not os.path.exists(sync_folder_path):
        os.mkdir(sync_folder_path)
    elif len(os.listdir(sync_folder_path)) != 0:
        shutil.rmtree(sync_folder_path)

    cameras_folder_path = scene_path + '\\' + sensor_folder_names[0]
    lidar_folder_path = scene_path + '\\' + sensor_folder_names[1] + '\\' + lidar_folder_names[0]
    radars_folder_path = scene_path + '\\' + sensor_folder_names[2]
    lidar_file_names = os.listdir(lidar_folder_path) #lidar文件名 列表 ’XXXXXXXXX.bin‘
    for j in range(len(lidar_file_names)):
        lidar.append(lidar_file_names[j][:16])
        lidar_time = lidar_file_names[j][:16][:10] + '.' + lidar_file_names[j][:16][10:] #lidar时间戳 'XXXXXX.XXX'
        for m in range(len(cameras_folder_names)):
            camera_flag = cameras_folder_names[m]
            camera_file_path = cameras_folder_path + '\\' + camera_flag
            camera_file_names = os.listdir(camera_file_path) #camera文件名 列表 ’XXXXXXXXX.jpg‘
            camera_diff_list = []
            for n in range(len(camera_file_names)):
                camera_time = camera_file_names[n][:16][:10] + '.' + camera_file_names[n][:16][10:] #camera时间戳 'XXXXXX.XXX'
                diff = eval(lidar_time) - eval(camera_time)
                camera_diff_list.append(abs(diff))
            camera_diff_min = min(camera_diff_list) #绝对值最小
            min_index = camera_diff_list.index(camera_diff_min) #最小值索引
            cameras_nearest.append(camera_file_names[min_index][:16])
        for p in range(len(radars_folder_names)):
            radar_flag = radars_folder_names[p]
            radar_file_path = radars_folder_path + '\\' + radar_flag
            radar_file_names = os.listdir(radar_file_path) #camera文件名 列表 ’XXXXXXXXX.bin‘
            radar_diff_list = []
            for q in range(len(radar_file_names)):
                radar_time = radar_file_names[q][:16][:10] + '.' + radar_file_names[q][:16][10:] #radar时间戳 'XXXXXX.XXX'
                diff = eval(lidar_time) - eval(radar_time)
                radar_diff_list.append(abs(diff))
            radar_diff_min = min(radar_diff_list)  # 绝对值最小
            min_index = radar_diff_list.index(radar_diff_min)  # 最小值索引
            radars_nearest.append(radar_file_names[min_index][:16])

        #生成字典
        cameras_nearest_dict = dict(zip(cameras_folder_names, cameras_nearest))
        radars_nearest_dict = dict(zip(radars_folder_names, radars_nearest))
        lidar_dict = dict(zip(lidar_folder_names, lidar))
        scene_dict = {'lidar': lidar_dict, 'cameras': cameras_nearest_dict, 'radars': radars_nearest_dict}

        #写入json
        sync_file_path = sync_folder_path + '\\' + lidar_file_names[j][:16] + '.json'
        with open(sync_file_path, 'w') as f:
            f.write(json.dumps(scene_dict, indent=4, ensure_ascii=False))

    # 显示进度条
    print("\r", end="")
    print("Progress: {}/{}: ".format(i+1, len(scenes_file_names)), "▋" * ((i+1) // 2),end="")
    sys.stdout.flush()
    time.sleep(0.05)