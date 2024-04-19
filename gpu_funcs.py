from numba import cuda

@cuda.jit
def sepiaToneGPU(img, size, filter, result):
    thread_id = cuda.grid(1)
    stride = cuda.gridsize(1)
    
    for i in range(thread_id, size, stride):
        result[i][0] = img[i][0]*filter[0][0] + img[i][1]*filter[1][0] + img[i][2]*filter[2][0]
        result[i][1] = img[i][0]*filter[0][1] + img[i][1]*filter[1][1] + img[i][2]*filter[2][1]
        result[i][2] = img[i][0]*filter[0][2] + img[i][1]*filter[1][2] + img[i][2]*filter[2][2]