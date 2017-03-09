from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import math

def main():
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	# Make data.
	X = np.arange(-40, 40, 0.1)
	Y = np.arange(-40, 40, 0.1)
	X, Y = np.meshgrid(X, Y)
	#https://en.wikipedia.org/wiki/Rosenbrock_function
	ai = []
	aj = []
	for i in range(0,25):
		if i % 5 == 0:
			ai.append(-32)
		elif i % 5 == 1:
			ai.append(-16)
		elif i % 5 == 2:
			ai.append(0)
		elif i % 5 == 3:
			ai.append(16)
		elif i % 5 == 4:
			ai.append(32)
		if i < 5:
			aj.append(-32)
		elif i < 10:
			aj.append(-16)
		elif i < 15:
			aj.append(0)
		elif i < 20:
			aj.append(16)
		elif i < 25:
			aj.append(32)
	hasil = []
	for i in range(1,26):
		hasil.append((i + (X - ai[i-1])**6 + (Y - aj[i-1])**6)**(-1))
	Z = (0.002 + sum(hasil))**(-1)
	# Plot the surface.
	surf = ax.plot_surface(X, Y, Z, cmap=cm.gist_stern,
	                       linewidth=0, antialiased=False)

	# Customize the z axis.
	#ax.set_zlim(-1.01, 1.01)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	# Add a color bar which maps values to colors.
	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()

main()