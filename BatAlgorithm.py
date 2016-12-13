import random 
from math import exp
import numpy as np

class BatAlgorithm():
    def __init__(self, Dim, NP, N_Gen, Qmin, Qmax, Alpha , Gama, Loudness, PulseRate, function):
        self.Dim = Dim  #Розмірність
        self.NP = NP  #Розмір популяції
        self.N_Gen = N_Gen  #Ітерації
        self.Qmin = Qmin  #Мінімальна частота
        self.Qmax = Qmax  #Максимальна частота
        self.Alpha = Alpha  
        self.Gama = Gama
        self.Loudness = Loudness       #гучність звукового сигналу
        self.PulseRate = PulseRate     #Інтенсивність звукового сигналу
        self.Lower = -5.12  #Нижня межа
        self.Upper = 5.12  #Верхня межа

        self.f_min = 0.0  

        self.Lb = [0] * self.Dim  
        self.Ub = [0] * self.Dim  
        self.Q = [0] * self.NP  #Частота кажанів
        self.A = [0] * self.NP #гучність
        self.r = [0] * self.NP #швидкіть поширення імпульсу

        self.v = [[0 for i in range(self.Dim)] for j in range(self.NP)]  #Швидкість кажанів
        self.Sol = [[0 for i in range(self.Dim)] for j in range(self.NP)]  #Положення кажанів (координати)
        self.Fitness = [0] * self.NP  # Здоровя
        self.average_health_history = [0]*self.N_Gen
        self.best = [0] * self.Dim  #Кращі кажанів (координати)
        self.Fun = function
        

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

        for t in range(self.N_Gen):
            for i in range(self.NP):
                rnd = random.uniform(0, 1)
                self.Q[i] = self.Qmin + (self.Qmin - self.Qmax) * rnd        
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

                rnd = random.random()

                if (Flocal <= self.Fitness[i]) and (rnd < self.A[i]):
                    for j in range(self.Dim):
                    	self.Sol[i][j] = S[i][j]
                    self.Fitness[i] = Flocal        
                    self.A[i] = self.A[i]*self.Alpha
                    self.r[i] = self.PulseRate*(1-exp(-self.Gama*(t)))

                if Flocal <= self.f_min:
                    for j in range(self.Dim):
                        self.best[j] = S[i][j]
                    self.f_min = Flocal
            self.average_health_history =[np.average(self.Fitness)]+self.average_health_history
            if(self.stop(t)):
                print("break!")
                break
                

        print(self.f_min) 
        print(self.best)

    def stop(self, t):
        if t>=4:
            resent_hist = self.average_health_history[t-4:t+1]
            if max(resent_hist) - min(resent_hist) < 0.01 and abs(self.f_min - np.average(self.Fitness))<0.01:
                return True
            else:
                return False
        else:
            return False