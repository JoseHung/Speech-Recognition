import numpy as np

def optimal_distortion():
    ref = [5,7,9,6,4,2,0,1,3,6]
    input = [1,3,5,8,4,3,4,2,5,1]
    dis_matrix = np.zeros((10,10))
    for x in range(10):
        for y in range(10):
            dis_matrix[x][y] = pow(ref[x] - input[y],2)
    accu_matrix = np.zeros((10,10))
    for x in range(10):
        for y in range(10):
            if(x == 0 and y == 0):
                accu_matrix[x][y] = dis_matrix[x][y]
            elif(x == 0):
                accu_matrix[x][y] = dis_matrix[x][y] + accu_matrix[x][y - 1]
            elif(y == 0):
                accu_matrix[x][y] = dis_matrix[x][y] + accu_matrix[x - 1][y]
            else:
                m = min(accu_matrix[x - 1][y],accu_matrix[x][y - 1],accu_matrix[x - 1][y - 1])
                accu_matrix[x][y] = dis_matrix[x][y] + m
    print(accu_matrix)
    

optimal_distortion()