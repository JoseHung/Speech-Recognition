import numpy as np
import math
import matplotlib.pyplot as plt

s = [1,4,5,6,4,3,1,5,7,9,5,4,3,6,7,8,7,4,0,2,3,6]
x_real = []
x_img = []
res = []
for m in range(22):
    tmp_real = 0
    tmp_img = 0
    for k in range(22):
        tmp_real = tmp_real + s[k] * math.cos(2 * math.pi * k * m / 22)
        tmp_img = tmp_img - s[k] * math.sin(2 * math.pi * k * m / 22)
    x_real.append(tmp_real)
    x_img.append(tmp_img)
    res.append(math.sqrt(math.pow(x_real[m],2) + math.pow(x_img[m],2)))
plt.plot(res)
plt.show()