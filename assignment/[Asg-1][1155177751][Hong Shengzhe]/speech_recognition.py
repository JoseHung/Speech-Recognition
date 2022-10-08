import librosa
import numpy as np
import math
import matplotlib.pyplot as plt

from pkg_resources import set_extraction_path

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

'''
# draw the path
s1A_data_path = '/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-A/s1A.wav'
s1B_data_path = '/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-B/s1B.wav'
mfccA = mfcc(s1A_data_path)
mfccB = mfcc(s1B_data_path)
score = optimal_distortion(mfccA, mfccB)
'''
# 1 读取文件夹中所有文件，分为 A 和 B 两类
# 2 得到两类 mfcc 参数
# 3 两两对比计算，得到score
# 4 画出score矩阵

# show an n × n Confusion matrix- table
# 得到所有的文件路径
setA_path = []
setB_path = []
for i in range(1,7):
    setA_path.append('/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-A/s' + str(i) + 'A.wav')
    setB_path.append('/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-B/s' + str(i) + 'B.wav')
# 得到所有文件的 mfcc 系数
mfccA = []
mfccB = []
for i in range(6):
    tmp = mfcc(setA_path[i])
    mfccA.append(tmp)
    tmp = mfcc(setB_path[i])
    mfccB.append(tmp)

# 两两计算 minimum accumulated distance 并得到 n × n Confusion matrix-table
score_matrix = []
for i in range(6):
    curLevel = []
    for j in range(6):
        tmp = optimal_distortion(mfccA[i], mfccB[j])
        curLevel.append(tmp)
    score_matrix.append(curLevel)
score_matrix = np.array(score_matrix)
plt.imshow(score_matrix, cmap=plt.cm.gray)
plt.colorbar()
plt.title("Confusion Matrix Table")
plt.xlabel('Reference Class)')
plt.ylabel('Predicted Class')
'''
# 可以显示具体数值
for i in range(6):
    for j in range(6):
        plt.text(x=j, y=i, s=int(score_matrix[i, j]))
'''
plt.show()