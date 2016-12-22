import random 
from math import exp
import numpy as np
import os
import spo

flag = False

class BatAlgorithmForSpo():
    def __init__(self,criterionsValueInt,x):
        self.Dim = 2
        self.NP = criterionsValueInt[1]
        self.N_Gen = criterionsValueInt[0]
        self.Qmin = criterionsValueInt[2]
        self.Qmax = criterionsValueInt[3]
        self.Alpha = criterionsValueInt[4]
        self.Gama = criterionsValueInt[5]

        self.Loudness = x[0]
        self.PulseRate = x[1]

        self.Lower = - 5.12  #Нижня межа
        self.Upper = 5.12  #Верхня межа

        self.iteration = 0

        self.count = 1   #лічильник для кількості викликів фітнес - функції

        self.f_min = 0.0  

        self.Lb = [0] * self.Dim  
        self.Ub = [0] * self.Dim  
        self.Q = [0] * self.NP  #Частота кажанів
        self.A = [0] * self.NP #гучність
        self.r = [0] * self.NP #швидкіть поширення імпульсу

        self.v = [[0 for i in range(self.Dim)] for j in range(self.NP)]  #Швидкість кажанів
        self.Sol = [[0 for i in range(self.Dim)] for j in range(self.NP)]  #Положення кажанів (координати)
        self.Fitness = [0] * self.NP  # Здоровя
        self.average_health_history = []   #Середнє здоров'я популяцій
        self.best = [0] * self.Dim  #Кращі кажанів (координати)
        self.average_best = []

    def Fun(self,Dim, sol):
      npSol = np.array(sol)
      return sum(100*(npSol[1:] - npSol[:-1]**2)**2 + (1 - npSol[:-1])**2)


    def best_bat(self):
        i = 0
        j = 0
        for i in range(self.NP):
            if self.Fitness[i] < self.Fitness[j]:   #Шукаємо мінімальне значення функції
                j = i
        for i in range(self.Dim):
            self.best[i] = self.Sol[j][i]         # Записуємо координати кращого кажана
        self.f_min = self.Fitness[j]

    def init_bat(self):
        try:
            os.mkdir("Information")
        except:
               pass
        TextFile = open(os.getcwd()+"\\Information\\"+"Population.txt", 'w')
        TextFile.close()
        for i in range(self.Dim):
            self.Lb[i] = self.Lower
            self.Ub[i] = self.Upper

        for i in range(self.NP):
            self.Q[i] = 0
            a = random.uniform(0,1)
            self.A[i] = self.Loudness       #Початкові значення гучності
            self.r[i] = self.PulseRate       #Початкові значення швидкості імпульсу
            for j in range(self.Dim):
                rnd = random.uniform(0, 1)
                self.v[i][j] = 0.0
                self.Sol[i][j] = self.Lb[j] + (self.Ub[j] - self.Lb[j]) * rnd #Випадковим чином генеруємо координати початкох кажанів
            self.Fitness[i] = self.Fun(self.Dim, self.Sol[i])
            self.count = self.count + 1
        self.best_bat()

    def simplebounds(self, val, lower, upper):
        if val < lower:
            val = lower
        if val > upper:
            val = upper
        return val

    def move_bat(self):
        S = [[0.0 for i in range(self.Dim)] for j in range(self.NP)]   #Положення кажанів

        self.init_bat()

        for self.iteration in range(self.N_Gen):
            for i in range(self.NP):
                rnd = random.uniform(0, 1)
                self.Q[i] = self.Qmin + (self.Qmax - self.Qmin) * rnd        
                for j in range(self.Dim):
                    self.v[i][j] = self.v[i][j] + (self.Sol[i][j] -
                                                   self.best[j]) * self.Q[i]  #Нова швидкість кажана	
                    S[i][j] = self.Sol[i][j] + self.v[i][j]                   #Нове положення кажана

                    S[i][j] = self.simplebounds(S[i][j], self.Lb[j],           
                                                self.Ub[j])

                rnd = random.random()

                if rnd > self.r[i]:
                    for j in range(self.Dim):
                        S[i][j] = self.best[j] + np.average(self.A) * random.uniform(-1, 1)    #Локальний пошук методом випадкового блукання  
                Flocal = self.Fun(self.Dim, S[i])
                self.count = self.count + 1

                rnd = random.random()

                if (Flocal <= self.Fitness[i]) and (rnd < self.A[i]):
                    for j in range(self.Dim):
                    	self.Sol[i][j] = S[i][j]
                    self.Fitness[i] = Flocal        
                    self.A[i] = self.A[i]*self.Alpha
                    self.r[i] = self.PulseRate*(1-exp(-self.Gama*(self.iteration)))

                if Flocal <= self.f_min:
                    for j in range(self.Dim):
                        self.best[j] = S[i][j]
                    self.f_min = Flocal

                if(flag):
                	break
            if(flag):
            	break

            self.average_health_history.append(np.average(self.Fitness))   # середнє здоров'я особин популяцій 
            self.average_best.append(self.f_min)    # - відхилення середнього знайденого розв’язку від оптимального 

            if self.stop(self.iteration):
                break
      
        print(self.f_min) 
        print(self.iteration)
        print(self.best)        

    def WritingInfo(self,t):
        my_file = open(os.getcwd()+"\\Information\\"+"Population.txt", 'a')
        my_file.write('\n')
        iterationStr = "Ітерація: {0}".format(t)
        my_file.write(iterationStr+'\n')
        my_file.write("Здоров'я кожного кажана в популяції: "+'\n')
        for h in range(self.NP):
            my_file.write(str(self.Fitness[h].item())+'\n')
        averageHealthPopulation = "Середнє здоров'я популяції: {0}".format(str(self.average_health_history[t].item()))
        my_file.write(averageHealthPopulation + '\n')
        bestBat = "Кращий кажан: {0}".format(self.best)
        minFunction = "Краще значення Фітнес-функції: {0}".format(self.f_min)
        my_file.write(bestBat + '\n')
        my_file.write(minFunction+'\n')
        dist = "Евклідова відстань: {0}".format(str(np.linalg.norm(self.best - np.array([1]*self.Dim))))
        my_file.write(dist+'\n')

        my_file.close()

    def WriteInToExcell():
        dist = np.linalg.norm(self.best - np.array([1]*self.Dim))
        strings= (str(self.iteration) + '\t' + str(self.count) + '\t'+str(self.f_min) + '\t'+str(np.average(self.average_best)) + '\t'+str(dist) + '\t')
        test = open("test.txt",'a')
        test.write(strings)
        test.close

    def getDeviationBestSolution(self):
    	return self.f_min


    def stop(self, t):
        if t>=4:
            resent_hist = self.average_health_history[t-4:t+1]
            if max(resent_hist) - min(resent_hist) < 0.0001 and abs(self.f_min - np.average(self.Fitness))<0.01:
                return True
            else:
                return False
        else:
            return False

         

                





        
