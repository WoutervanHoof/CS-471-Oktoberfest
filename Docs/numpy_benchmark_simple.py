import numpy as np
from time import time

np.__config__.show()
np.random.seed(0)

size = 16
A, B = np.random.rand(size, size), np.random.rand(size, size)

N = 20
t = time()
for i in range(N):
    np.dot(A, B)
delta = time() - t
print('Dotted two %dx%d matrices in %0.2f s.' % (size, size, delta / N))
