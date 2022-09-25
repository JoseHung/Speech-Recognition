import wave
import matplotlib.pyplot as plt
import numpy as np
with wave.open('/Users/josehung/Downloads/document/course/CMSC5707/assignment/[Asg-1][1155177751][Hong Shengzhe]/set-A/s1A.wav') as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()
    print('sampling rate:', framerate, 'Hz')
    print('length:', frames, 'samples')
    print('channels:', channels)
    print('sample width:', width, 'bytes')
    
    data = w.readframes(frames)
np.frombuffer(data, dtype='B')
sig = np.frombuffer(data, dtype='<i2').reshape(-1, channels)
plt.plot(sig)
plt.show()