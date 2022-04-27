# import libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as circle
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# size of matrix
n = 10

# create n x n random matrix of naturals
A = np.random.randint(1,10, size=(n,n))

evals, evectors = np.linalg.eig(A)
norm = np.zeros(len(evals))
for i in range(len(evals)):
    norm[i] = np.absolute(evals[i])
plt.scatter(evals.real, evals.imag,s=10)
plt.xlim(-10,60)
plt.xlabel(r"Real part",size=11)
plt.ylabel(r"Imaginary part",size=11)
plt.title(r"Eigenvalues in the complex plane",size=11)
circle = plt.Circle((0,0),radius = np.max(norm), \
                    fill=False, color='r')
plt.gca().add_patch(circle)
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('motivation.pdf', format="pdf")
plt.show()
index = np.argmax(norm)
print(np.real(max(evals)))
print(evectors[:,index])

if len(A.shape) > 2:
        raise ValueError('bmatrix can at most display two dimensions')
temp_string = np.array2string(A, formatter={'float_kind':lambda x: "{:.2e}".format(x)})
lines = temp_string.replace('[', '').replace(']', '').splitlines()
rv = [r'\begin{pmatrix}']
rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
rv +=  [r'\end{pmatrix}']
print('\n'.join(rv))
