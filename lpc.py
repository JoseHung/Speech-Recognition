import numpy as np

def lpc_coeff():
    # 这一部分是计算 auto-correlation parameters
    sig = np.array([1,2,6,2,6,7,2,8,3,4,6,7,8,5,8]) # 样本数据
    auto_coeff = np.array([0,0,0,0,0]) # lpc参数长度
    i = 0
    while i <= 4:
        j = i
        while j < 15:
            auto_coeff[i] += sig[j] * sig[j-i]
            j += 1
        i += 1
    print(auto_coeff)
    a = np.array([[461,348,359,324], [348,461,348,359],[359,348,461,348],[324,359,348,461]])
    b = np.array([348,359,324,254])
    inverse = np.linalg.inv(a)
    lpccoeff = np.dot(b, inverse)
    print(lpccoeff)






lpc_coeff()