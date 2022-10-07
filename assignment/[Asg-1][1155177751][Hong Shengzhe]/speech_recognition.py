import librosa
import numpy as np
import math

# 计算mfcc系数
def mfcc(data_path):
    y, sr = librosa.load(data_path, sr=44100)
    # 提取 MFCC feature
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfccs

# 计算optimal_distortion
def optimal_distortion(mfccA, mfccB):
    # 得到 mfccA 中的 t 的数量 lenA
    # 得到 mfccB 中的 t 的数量 lenB
    # 将表格格式设置为 lenA * lenB
    lenA = len(mfccA[0])
    lenB = len(mfccB[0])
    # 得到 distortion score matrix
    dis_matrix = np.zeros((lenA,lenB))
    for x in range(lenA): 
        for y in range(lenB):
            sum = 0
            for j in range(1,12):
                sum += (mfccA[j, x] - mfccB[j, y]) * (mfccA[j, x] - mfccB[j, y])
            dis_matrix[x][y] = math.sqrt(sum)
    # 得到 accumulated distortion score matrix
    accu_matrix = np.zeros((lenA,lenB))
    for x in range(lenA):
        for y in range(lenB):
            if(x == 0 and y == 0):
                accu_matrix[x][y] = dis_matrix[x][y]
            elif(x == 0):
                accu_matrix[x][y] = dis_matrix[x][y] + accu_matrix[x][y - 1]
            elif(y == 0):
                accu_matrix[x][y] = dis_matrix[x][y] + accu_matrix[x - 1][y]
            else:
                m = min(accu_matrix[x - 1][y],accu_matrix[x][y - 1],accu_matrix[x - 1][y - 1])
                accu_matrix[x][y] = dis_matrix[x][y] + m
    # 找到最小值
    min1 = accu_matrix[lenA - 1][0]
    point1 = [lenA - 1, 0]
    for i in range(lenB):
        if min1 > accu_matrix[lenA - 1][i]:
            min1 = accu_matrix[lenA - 1][i]
            point1[1] = i
    min2 = accu_matrix[0][lenB - 1]
    point2 = [0, lenB - 1]
    for i in range(lenA):
        if min2 > accu_matrix[i][lenB - 1]:
            min2 = accu_matrix[i][lenB - 1]
            point2[0] = i
    min_score = 0
    point = []
    if min1 <= min2:
        min_score = min1
        point = point1
    else:
        min_score = min2
        point = point2
    return min_score


s1A_data_path = '/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-A/s1A.wav'
s1B_data_path = '/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-B/s1B.wav'
mfccA = mfcc(s1A_data_path)
mfccB = mfcc(s1B_data_path)
score = optimal_distortion(mfccA, mfccB)