from dataclasses import dataclass
import numpy as np

def binary_Kmeans():
    p = [[1.1,2.1],[0.3,0.7],[0.2,0.6],[1.4,5.6],[4.5,7.8],[2.3,2.6],[5.5,5.6],[5.7,8.9],[1.2,3.4],[4.5,4.7]]
    i = 0
    sumx = 0
    sumy = 0
    while i <= 9:
        sumx += p[i][0]
        sumy += p[i][1]
        i += 1
    c = np.array([sumx / 10, sumy / 10])
    cca = np.array([c[0] * 1.01, c[1] * 1.01])
    ccb = np.array([c[0] * 0.99, c[1] * 0.99])
    a = []
    b = []
    for point in p:
        disxa = point[0] - cca[0]
        disya = point[1] - cca[1]
        disxb = point[0] - ccb[0]
        disyb = point[1] - ccb[1]
        da = pow(disxa,2) + pow(disya,2)
        db = pow(disxb,2) + pow(disyb,2)
        if(da <= db):
            a.append(point)
        else:
            b.append(point)
    sumx = 0
    sumy = 0
    for pa in a:
        sumx += pa[0]
        sumy += pa[1]
    c1 = [sumx / 5, sumy/5]
    sumx = 0
    sumy = 0
    for pb in b:
        sumx += pb[0]
        sumy += pb[1]
    c2 = [sumx / 5, sumy/5]
    print(c1[0]+c1[1]+c2[0]+c2[1])
    


binary_Kmeans()