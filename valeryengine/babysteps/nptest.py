import numpy as np


m = np.fromfunction(lambda i, j: (i +1)* 10 + j + 1, (9, 4), dtype=int)

print(m[::2, 0])
#