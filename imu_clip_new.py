import os
import sys
import time
import xlrd
from datetime import datetime, timedelta

# 硬编码的路径
imu_file_path = r'F:\10.6示例数据\2023-09-03-14-57-42_1\imu_data.txt'
output_folder = r'F:\10.6示例数据\2023-09-03-14-57-42_1\clip_data'

clip_lidar_timestamp_path = os.path.join(output_folder, 'clip_lidar_timestamp.xls')
clip_timestamp = xlrd.open_workbook(clip_lidar_timestamp_path).sheets()[0]
clip_start_timestamp_list = clip_timestamp.col_values(0)
clip_end_timestamp_list = clip_timestamp.col_values(1)

# 读取 IMU 数据
imu_data = []
imu_time = []
with open(imu_file_path, 'r', encoding='utf-8') as imu:
    for line in imu:
        data = line[:-1]  # 去掉换行符
        timestamp = data.split(',')[0]
        timestamp = timestamp[:10] + '.' + timestamp[10:]
        imu_data.append(data)
        imu_time.append(timestamp)

# 计算时间范围
imu_start_time = eval(imu_time[0])
imu_end_time = eval(imu_time[-1])

for i in range(len(clip_start_timestamp_list)):
    start_time = eval(clip_start_timestamp_list[i])
    end_time = eval(clip_end_timestamp_list[i])

    # 计算时间范围
    start_time -= 1
    end_time += 1

    # 找到 IMU 数据在时间范围内的索引
    start_index = 0
    end_index = len(imu_time)

    for j, timestamp in enumerate(imu_time):
        if eval(timestamp) >= start_time:
            start_index = j
            break

    for j, timestamp in enumerate(imu_time[start_index:]):
        if eval(timestamp) > end_time:
            end_index = start_index + j
            break

    clip_seq = imu_data[start_index:end_index]

    # 写入 IMU 文件
    imu_path = os.path.join(output_folder, f'{clip_start_timestamp_list[i][:10]}{clip_start_timestamp_list[i][11:]}',
                            'imu.txt')
    imu_txt = '\n'.join(clip_seq)

    with open(imu_path, 'w', encoding='utf-8') as f:
        f.write(imu_txt)

    # 显示进度条
    print("\r", end="")
    print("Progress: {}/{}: ".format(i + 1, len(clip_start_timestamp_list)), "▋" * ((i + 1) // 2), end="")
    sys.stdout.flush()
    time.sleep(0.05)
