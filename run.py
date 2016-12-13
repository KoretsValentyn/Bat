import random
from BatAlgorithm import *
import numpy as np

def Sphere(Dim, sol):
	npSoll=np.array(sol)
	val = 0.0
	for i in range(Dim):
		val = val + npSoll[i] * npSoll[i]
	return val


def Rosenbrock(Dim, sol):
	npSol = np.array(sol)
	return sum(100*(npSol[1:] - npSol[:-1]**2)**2 + (1 - npSol[:-1])**2)



for i in range(1):
    Algorithm = BatAlgorithm(4, 40, 1000, 0.0, 2.0, -5.12, 5.12, Rosenbrock)
    #Algorithm = BatAlgorithm(2, 40, 1000, 0.0, 2.0, -10.0, 10.0, Sphere)
    Algorithm.move_bat()

