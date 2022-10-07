import librosa

#计算mfcc系数
def mfcc():
    y, sr = librosa.load('/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-A/s1A.wav', sr=44100)
    # 提取 MFCC feature
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    print(mfccs.shape)