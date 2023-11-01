import os
from collections import defaultdict


def myfunction(folder_path):

    # 检查文件夹是否存在
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("文件夹路径无效")
    else:
        # 创建一个字典来存储记录频率
        record_frequency = defaultdict(int)

        # 遍历文件夹中的文件
        for filename in os.listdir(folder_path):
            # 假设文件名的格式为时间戳，这里可以根据实际情况进行调整
            try:
                timestamp = eval((filename[:16]))
                record_frequency[timestamp] += 1
            except ValueError:
                print(f"文件名无效: {filename}")

        return record_frequency

scenes_folder_path = r'F:\10.6示例数据\2023-09-03-14-57-42_1\clip_data' #切片后的文件夹
scenes_file_names = os.listdir(scenes_folder_path) #切片scenes的文件名列表 '...../XXXXXXXXXX'
sensor_folder_names = ['cameras', 'lidar', 'radars', 'imu']
cameras_folder_names = ['CAMERA_LEFT_FRONT',
                        'CAMERA_LEFT_REAR',
                        'CAMERA_RIGHT_REAR',
                        'CAMERA_RIGHT_FRONT',
                        'CAMERA_FRONT',
                        'CAMERA_REAR']
lidar_folder_names = ['LIDAR_TOP']
radars_folder_names = ['RADAR_LEFT_FRONT',
                       'RADAR_FRONT',
                       'RADAR_RIGHT_FRONT',
                       'RADAR_LEFT_REAR',
                       'RADAR_REAR',
                       'RADAR_RIGHT_REAR']


