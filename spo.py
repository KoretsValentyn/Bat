import math
import BatAlgorithmForSpo
import random


criterionsValueInt = [1000, 40, 2.0, 2.0,0.9,0.9] #iteration population, Qmin, Qmax, Alpha , Gama

class SPO():
	maxSteps = 100
	EPS = 0.000001
	GLOBAL_MIN = 0
	criterionsValueInt = {}

	def evolution(self,xp0,sigma0,a,g,rng,criterionsValue):
		criterionsValueInt = criterionsValue
		step = 0
		xo = 0
		yo = 0
		xp = xp0
		yp = math.inf
		sigma = sigma0
		n = xp0.dimention()
		mutationHistory = self.MutationHistory(g)
		yp = self.valueOf(xp.data)

		while(step < self.maxSteps and abs(yp - self.GLOBAL_MIN) >= self.EPS ):
			print("xp: {0}".format(xp))
			print("yp: {0}".format(str(yp)))

			#xo = xp.plus(self.RealVector.gaussianRandom(self,n,rng).timeScalar(sigma))
			temp = self.RealVector.gaussianRandom(self,n,rng)
			xo = xp.plus(temp.timeScalar(sigma))
			xo.normalizeVector()
			yo = self.valueOf(xo.data)

			if(yo <yp):
				mutationHistory.recordSuccess()
				xp = xo
				yp = yo
				print("improving: step {0} parameters {1}".format(str(step),str(xp)))
				print("improving:  {0} parameters {1}".format(str(step),str(yp)))
			else:
				mutationHistory.recordFailure()
			successRate = mutationHistory.successRate()
			if(successRate >0.2):
				sigma = sigma * a
			elif(successRate<0.2):
				sigma = sigma/a
				#sigma(t+1) = sigma(t)
			else:
				sigma = sigma
			step = step + 1
		print("xp: {0}".format(str(xp)))
		print("yp: {0}".format(str(yp)))
		return self.IndividualFitnessPair(xp,yp)

	def valueOf(self,x):
		Algorithm = BatAlgorithmForSpo.BatAlgorithmForSpo(criterionsValueInt, x)
		Algorithm.move_bat()
		return Algorithm.getDeviationBestSolution()


	class RealVector():
		def __init__(self,data):
			self.data = data

		def dimention(self):
			return len(self.data)

		def normalizeVector(self):
			self.data[0] = abs(self.data[0] - int(self.data[0]))
			self.data[1] = abs(self.data[1] - int(self.data[1]))
	
		def plus(self,other):
			sumData = [0]*self.dimention()
			count = 0
			for i in sumData:
				sumData[count] = self.data[count]+other.data[count]
				count = count + 1
			testP = SPO.RealVector(sumData)
			return testP

		def timeScalar(self,scalar):
			scalarProductData = [0]*self.dimention()
			count = 0
			for i in scalarProductData:
				scalarProductData[count] = scalar*self.data[count]
				count = count+1
			testS = SPO.RealVector(scalarProductData)
			return testS


		def gaussianRandom(self,dimention,rng):
			randomData = [0]*dimention
			count = 0
			for i in randomData:
				randomData[count] = random.uniform(-1,1)
				count = count+1
			test = self.RealVector(randomData)
			return test

		def __str__(self):
			return str(self.data)


	class IndividualFitnessPair():
		def __init__(self,individual, fitness):
			self.individual = individual
			self.fitness = fitness

		def __str__(self):
			return "<individual: {0}\n fitness: {1}>".format(str(self.individual),str(selffitness))

	class MutationHistory():
		def __init__(self,g):
			self.g = g
			self.historyList = []

		def record(self,successful):
			if successful:
				self.historyList.insert(0,1)
			else:
				self.historyList.insert(0,0)

			if(len(self.historyList)>self.g):
				self.historyList.pop()

		def recordSuccess(self):
			self.record(True)

		def recordFailure(self):
			self.record(False)

		def successRate(self):
			gSuccessful = 0.0
			for elt in self.historyList:
				gSuccessful = gSuccessful + elt
			return gSuccessful/len(self.historyList)
def main():
	rng = random.uniform(-1,1)
	initial = [0.5,0.5]    #loudness, pulseRate
	test = SPO()
	xp0 = test.RealVector(initial)
	sigma0 = 0.3
	a = 1.3
	g = 2
	runResult = test.evolution(xp0, sigma0, a, g, rng, criterionsValueInt)
	print(runResult.individual)
	print(runResult.fitness)

if __name__ == "__main__":
   main()




















