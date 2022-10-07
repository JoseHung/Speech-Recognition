# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
import math

def sgn(data):
    if data >= 0 :
        return 1
    else :
        return 0

# 计算每一帧的能量 512个采样点为一帧
def calEnergy(wave_data) :
    energy = []
    sum = 0
    for i in range(len(wave_data)) :
        sum = sum + (wave_data[i] * wave_data[i])
        if (i + 1) % 512 == 0 :
            energy.append(sum)
            sum = 0
        elif i == len(wave_data) - 1 :
            energy.append(sum)
    return energy

#计算过零率
def calZeroCrossingRate(wave_data) :
    zeroCrossingRate = []
    sum = 0
    for i in range(len(wave_data)) :
        if i % 512 == 0:
            continue
        sum = sum + np.abs(sgn(wave_data[i]) - sgn(wave_data[i - 1]))
        if (i + 1) % 512 == 0 :
            zeroCrossingRate.append(float(sum) / 511)
            sum = 0
        elif i == len(wave_data) - 1 :
            zeroCrossingRate.append(float(sum) / 511)
    return zeroCrossingRate

# 利用短时能量，短时过零率，使用双门限法进行端点检测
def endPointDetect(wave_data, energy, zeroCrossingRate) :
    sum = 0
    energyAverage = 0
    for en in energy :
        sum = sum + en
    energyAverage = sum / len(energy)

    sum = 0
    for en in energy[:5] :
        sum = sum + en
    ML = sum / 5                        
    MH = energyAverage / 4              #较高的能量阈值
    ML = (ML + MH) / 4    #较低的能量阈值
    print(ML)
    sum = 0
    for zcr in zeroCrossingRate[:5] :
        sum = float(sum) + zcr             
    Zs = sum / 5                     #过零率阈值
    A = []

    # 首先利用较大能量阈值 MH 进行初步检测
    flag = 0
    for i in range(len(energy)):
        if len(A) == 0 and flag == 0 and energy[i] > ML and zeroCrossingRate[i] > 1 * Zs :
            A.append(i)
            flag = 1
        elif flag == 0 and energy[i] > ML and i - 21 > A[len(A) - 1] and zeroCrossingRate[i] > 1 * Zs :
            A.append(i)
            flag = 1
        elif flag == 0 and energy[i] > ML and i - 21 <= A[len(A) - 1] and zeroCrossingRate[i] > 1 * Zs :
            A = A[:len(A) - 1]
            flag = 1
        if flag == 1 and (energy[i] < ML or zeroCrossingRate[i] < 1 * Zs) :
            A.append(i)
            flag = 0
    print("较高能量阈值, 计算后的浊音A:" + str(A))
    start = A[0] * 512
    end = A[1] * 512
#    plt.plot(wave_data)
#    plt.axvline(start, c = 'r')
#    plt.axvline(end, c = 'r')
#    plt.text(start, 0, 'T1', c = 'r')
#    plt.text(end, 0, 'T2', c = 'r')
    seg_start = start + 20000
    seg_end = start + 20882
#    plt.axvline(seg_start, c = 'y')
#    plt.axvline(seg_end, c = 'y')
#    plt.text(seg_end, 0, 'Seg1', c = 'y')
    Seg1 = []
    for i in range(882):
        Seg1.append(wave_data[start + 20000 + i])
    return Seg1
    
def fourierTransform(Seg1):
    res = []
    x_real = []
    x_img = []
    for m in range(882):
        tmp_real = 0
        tmp_img = 0
        for k in range(882):
            tmp_real = tmp_real + Seg1[k] * math.cos(2 * math.pi * k * m / 882)
            tmp_img = tmp_img - Seg1[k] * math.sin(2 * math.pi * k * m / 882)
        x_real.append(tmp_real)
        x_img.append(tmp_img)
        res.append(math.sqrt(x_real[m] * x_real[m] + x_img[m] * x_img[m]))
    plt.plot(res)
    plt.xlabel('frequency')
    plt.ylabel('energy')
    plt.show()
    return res

def pre_em(Seg1):
    pre_Seg1 = []
    pre_Seg1.append(Seg1[0])
    len = 882
    for k in range(1, len):
        pre_Seg1.append(Seg1[k] - 0.95 * Seg1[k - 1])
    return pre_Seg1

f = wave.open("/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-A/s1A.wav","rb")
# getparams() 一次性返回所有的WAV文件的格式信息
params = f.getparams()
# nframes 采样点数目
nchannels, sampwidth, framerate, nframes = params[:4]
# readframes() 按照采样点读取数据
str_data = f.readframes(nframes)            # str_data 是二进制字符串

# 以上可以直接写成 str_data = f.readframes(f.getnframes())

# 转成二字节数组形式（每个采样点占两个字节）
wave_data = np.fromstring(str_data, dtype = np.short)
wave_data = wave_data * 1.0 / (max(abs(wave_data)))  # wave幅值归一化
print( "采样点数目：" + str(len(wave_data)))          #输出应为采样点数目
f.close()
energy = calEnergy(wave_data)
zeroCrossingRate = calZeroCrossingRate(wave_data)
Seg1 = endPointDetect(wave_data, energy, zeroCrossingRate)
pre_Seg1 = pre_em(Seg1)
plt.subplot(2,1,1)
plt.plot(Seg1)
plt.title("Seg1")
plt.subplot(2,1,2)
plt.plot(pre_Seg1)
plt.title("Pem_Seg1")
plt.show()
#FT = fourierTransform(Seg1)