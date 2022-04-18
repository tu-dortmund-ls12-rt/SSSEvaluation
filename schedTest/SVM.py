from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
from numpy.ma.core import sqrt


X = np.array([[1,1],[1,3],[1,5],[3,3],[8,1],[8,5],[10,1],[10,3],[10,5]])
y = np.array([-1,-1, -1, -1, 1, 1 , 1 ,1,1])

#clf = SVC(C = 1e5, kernel = 'linear')

clf=SVC(C = 1e5, kernel = 'linear')
clf.fit(X, y)


w = clf.coef_[0]
max=2/sqrt(pow(w[0],2)+pow(w[1],2))

print('w = ',clf.coef_)
print('maximum width = ',max)
print('b = ',clf.intercept_)
print('Indices of support vectors = ', clf.support_)
print('Support vectors = ', clf.support_vectors_)
print('Number of support vectors for each class = ', clf.n_support_)
print('Coefficients of the support vector in the decision function = ', np.abs(clf.dual_coef_))

plt.scatter(X[:, 0], X[:, 1], c = y)
# plot the decision function
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# plot decision boundary and margins
ax.contour(
    XX, YY, Z, colors="k", levels=[-1, 0, 1], alpha=0.5, linestyles=["--", "-", "--"]
)
# plot support vectors
ax.scatter(
    clf.support_vectors_[:, 0],
    clf.support_vectors_[:, 1],
    s=100,
    linewidth=1,
    facecolors="none",
    edgecolors="k",
)
plt.show()