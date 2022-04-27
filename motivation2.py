'''
Random positive
'''

# import libraries

import numpy as np
import matplotlib.pyplot as plt
import sys

# size of matrix
n = 100

maximum = 100

# create matrix
A = np.random.uniform(sys.float_info.min,maximum,size=(n,n))

evals = np.linalg.eigvals(A)
norm = np.zeros(len(evals))
for i in range(len(evals)):
    norm[i] = np.absolute(evals[i])
plt.scatter(evals.real, evals.imag,s=10)
plt.xlabel("Real part")
plt.ylabel("Imaginary part")
plt.title("Eigenvalues in the complex plane")
plt.grid(True)
plt.savefig('motivation2.png', format="png", \
            dpi=2400, bbox_inches = 'tight')
plt.show()
