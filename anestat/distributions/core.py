import numpy as np

x = np.array([1,2,3,4,5])
y = np.array([4,7,2,6,8])
z = np.array([3,6,2,4,1])

q = np.vstack([x,y,z])

print(np.linalg.eigvals(np.cov(q)))
