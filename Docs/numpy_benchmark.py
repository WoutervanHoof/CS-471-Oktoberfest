import numpy as np
from time import time

np.__config__.show()
np.random.seed(0)

size = 4096
A, B = np.random.rand(size, size), np.random.rand(size, size)


N = 20
t = time()
print(t)
for i in range(N):
    np.dot(A, B)

    # print the timestamp since the start of the loop
    print(time() - t)

delta = time() - t
print('Dotted two %dx%d matrices in %0.2f s.' % (size, size, delta / N))