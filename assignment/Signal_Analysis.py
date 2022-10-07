import wave
import numpy as np
import matplotlib.pyplot as plt


def read(data_path):
    '''读取语音信号
    '''
    wavepath = data_path
    f = wave.open(wavepath, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]  # 声道数、量化位数、采样频率、采样点数
    # print(nchannels)
    str_data = f.readframes(nframes)  # 读取音频，字符串格式
    f.close()
    wavedata = np.fromstring(str_data, dtype=np.int32)  # 将字符串转化为浮点型数据
    wavedata = wavedata * 1.0 / (max(abs(wavedata)))  # wave幅值归一化
    return wavedata, nframes, framerate


def plot(data, time):
    plt.plot(time, data)
    plt.grid('on')
    plt.show()


def enframe(data, win, inc):
    '''对语音数据进行分帧处理
    input:data(一维array):语音信号
          wlen(int):滑动窗长
          inc(int):窗口每次移动的长度
    output:f(二维array)每次滑动窗内的数据组成的二维array
    '''
    nx = len(data)  # 语音信号的长度
    try:
        nwin = len(win)
    except Exception as err:
        nwin = 1
    if nwin == 1:
        wlen = win
    else:
        wlen = nwin
    nf = int(np.fix((nx - wlen) / inc) + 1)  # 窗口移动的次数
    # print('窗口数:',nf)
    f = np.zeros((nf, wlen))  # 初始化二维数组
    indf = [inc * j for j in range(nf)]
    indf = (np.mat(indf)).T
    inds = np.mat(range(wlen))
    indf_tile = np.tile(indf, wlen)
    inds_tile = np.tile(inds, (nf, 1))
    mix_tile = indf_tile + inds_tile
    f = np.zeros((nf, wlen))
    for i in range(nf):
        for j in range(wlen):
            f[i, j] = data[mix_tile[i, j]]
    return f


def point_check(wavedata, win, inc):
    '''语音信号端点检测
    input:wavedata(一维array)：原始语音信号
    output:StartPoint(int):起始端点
           EndPoint(int):终止端点
    '''
    # 1.计算短时过零率
    FrameTemp1 = enframe(wavedata[0:-1], win, inc)
    FrameTemp2 = enframe(wavedata[1:], win, inc)
    signs = np.sign(np.multiply(FrameTemp1, FrameTemp2))  # 计算每一位与其相邻的数据是否异号，异号则过零
    signs = list(map(lambda x: [[i, 0][i > 0] for i in x], signs))
    signs = list(map(lambda x: [[i, 1][i < 0] for i in x], signs))
    diffs = np.sign(abs(FrameTemp1 - FrameTemp2) - 0.01)
    diffs = list(map(lambda x: [[i, 0][i < 0] for i in x], diffs))
    zcr = list((np.multiply(signs, diffs)).sum(axis=1))
    # 2.计算短时能量
    amp = list((abs(enframe(wavedata, win, inc))).sum(axis=1))
    print('max-index',amp.index(max(amp)))
    #    # 设置门限
    #    print('设置门限')
    ZcrLow = max([round(np.mean(zcr) * 0.1), 3])  # 过零率低门限
    ZcrHigh = max([round(max(zcr) * 0.1), 5])  # 过零率高门限
    AmpLow = min([min(amp) * 10, np.mean(amp) * 0.2, max(amp) * 0.1])  # 能量低门限
    AmpHigh = max([min(amp) * 10, np.mean(amp) * 0.2, max(amp) * 0.1])  # 能量高门限
    # 端点检测
    MaxSilence = 8  # 最长语音间隙时间
    MinAudio = 16  # 最短语音时间
    Status = 0  # 状态0:静音段,1:过渡段,2:语音段,3:结束段
    HoldTime = 0  # 语音持续时间
    SilenceTime = 0  # 语音间隙时间
    print('开始端点检测')
    StartPoint = 0
    for n in range(len(zcr)):
        if Status == 0 or Status == 1:
            if amp[n] > AmpHigh or zcr[n] > ZcrHigh:
                StartPoint = n - HoldTime
                Status = 2
                HoldTime = HoldTime + 1
                SilenceTime = 0
            elif amp[n] > AmpLow or zcr[n] > ZcrLow:
                Status = 1
                HoldTime = HoldTime + 1
            else:
                Status = 0
                HoldTime = 0
        elif Status == 2:
            if amp[n] > AmpLow or zcr[n] > ZcrLow:
                HoldTime = HoldTime + 1
            else:
                SilenceTime = SilenceTime + 1
                if SilenceTime < MaxSilence:
                    HoldTime = HoldTime + 1
                elif (HoldTime - SilenceTime) < MinAudio:
                    Status = 0
                    HoldTime = 0
                    SilenceTime = 0
                else:
                    Status = 3
        elif Status == 3:
            break
        if Status == 3:
            break
    HoldTime = HoldTime - SilenceTime
    EndPoint = StartPoint + HoldTime
    print(HoldTime)
    return StartPoint, EndPoint, FrameTemp1


if __name__ == '__main__':
    data_path = 'train/0.wav'
    win = 960
    inc = 480
    wavedata, nframes, framerate = read(data_path)
    # print(nframes, framerate)
    time_list = np.array(range(0, nframes)) * (1.0 / framerate)
    FrameTemp1 = enframe(wavedata[0:-1], win, inc)
    StartPoint, EndPoint, FrameTemp = point_check(wavedata, win, inc)
    print(StartPoint,EndPoint)
    print((StartPoint*480+960)* (1.0 / framerate),(EndPoint*480+960)* (1.0 / framerate))
    plt.plot(time_list, wavedata)
    plt.vlines((StartPoint*480+960)* (1.0 / framerate),-1,1,colors='r', linestyles='dashed', label='垂直线')
    plt.vlines((EndPoint*480+960)* (1.0 / framerate),-1,1 ,colors='r', linestyles='dashed', label='垂直线')
    plt.grid('on')
    plt.show()