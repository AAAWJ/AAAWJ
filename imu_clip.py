import os
import time
import sys
import xlrd

imu_file_path = r'F:\9.4_extract_rawdata\imu\20230904_133913\ins\ins1\chc_ins.txt'

clip_lidar_timestamp_path = r'G:\9.4clip_data\2023-09-04-13-47-56_1\clip_timestamp.xls'
clip_timestamp = xlrd.open_workbook(clip_lidar_timestamp_path).sheets()[0]
clip_start_timestamp_list = clip_timestamp.col_values(0) #列表[‘XXXXX.XXX’,...]
clip_end_timestamp_list = clip_timestamp.col_values(1) #列表[‘XXXXX.XXX’,...]

#读取imu文件存入list
imu_data = []
imu_time = []
with open(imu_file_path, 'r', encoding='utf-8') as imu:
    for line in imu:
        data = line[:-1]  # 去掉换行符
        timestamp = data.split(',')[0] #'XXXXXXXXXXX'
        timestamp = timestamp[:10] + '.' + timestamp[10:]  # 'XXXXXX.XXX'
        imu_data.append(data)
        imu_time.append(timestamp)

#跳过起始/结束多余数据
diff_1 = eval(imu_time[0]) - eval(clip_start_timestamp_list[0]) #防止最开始有不足1s的数据
index_1 = int(abs(diff_1)) * 100
diff_2 = eval(imu_time[-1]) - eval(clip_end_timestamp_list[-1]) - 5 #防止最末有不足1s的数据
index_2 = len(imu_time) - int(abs(diff_2)) * 100
imu_data = imu_data[index_1: index_2]
imu_time = imu_time[index_1: index_2]

m = 0
n = len(imu_time)
for i in range(len(clip_start_timestamp_list)):
    start_time = clip_start_timestamp_list[i]  # 起
    end_time = clip_end_timestamp_list[i]  # 终
    # 创建imu文件
    imu_path = 'G:/9.4clip_data/2023-09-04-13-47-56_1/' + start_time[:10] + start_time[11:] + '/imu.txt'
    imu_txt = ''
    #data_seq = imu_data[start_index:end_index]
    time_seq = imu_time[m:n]
    data_seq = imu_data[m:n]
    # -1时间-起始<0
    # 0<时间-终止<1
    # 起始<=time<=终止
    start = eval(start_time) - 1
    end = eval(end_time) + 1
    diff_start = [abs(eval(item)-start) for item in time_seq]
    diff_end = [abs(eval(item)-end) for item in time_seq]
    start_index = diff_start.index(min(diff_start))
    end_index = diff_end.index(min(diff_end))
    if end_index == -1 or end_index == len(time_seq) - 1:
        clip_seq = data_seq[start_index:]
    else:
        clip_seq = data_seq[start_index:end_index+1]
    #核对
    print('\nline num:', len(clip_seq))
    print('\nm:', m, '\tn:', n)
    print('\nstart_index:', start_index, '\tend_index:', end_index)
    #写入txt
    for k in clip_seq:
        imu_txt = imu_txt + k + '\n'
    with open(imu_path, 'w', encoding='utf-8') as f:
        f.write(imu_txt)
    if end_index == -1 or end_index == len(time_seq) - 1:
        print(min(diff_end))
        break
    m = m + end_index + 1 - 2*100 #提前2s
    #显示进度条
    print("\r", end="")
    print("Progress: {}/{}: ".format(i + 1, len(clip_start_timestamp_list)), "▋" * ((i + 1)//2), end="")
    sys.stdout.flush()
    time.sleep(0.05)