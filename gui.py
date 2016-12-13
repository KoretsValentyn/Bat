import random
from BatAlgorithm import *
import numpy as np
from tkinter import*
from tkinter import messagebox

class Gui( Frame ):
   def __init__( self ):
      Frame.__init__( self )
      self.master.title( "Bat" )

      self.master.rowconfigure( 0, weight = 1 )
      self.master.columnconfigure( 0, weight = 1 )
      self.grid( sticky = W+E+N+S )

      self.DimentionLb = Label(self, text="Dimention: ")
      self.PopulationLb = Label(self, text="Population: ")
      self.MinFrequencyLb = Label(self, text="Min Frequency: ")
      self.MaxFrequencyLb = Label(self, text="MaxFrequency: ")
      self.IteretionLb = Label(self, text = "Iteration: ")
      self.AlphaLb = Label(self, text = "Alpha: ")
      self.GamaLb = Label(self, text = "Gamma: ")
      self.LoudnessLb = Label(self, text = "Loudness: ")
      self.PulseRateLb = Label(self, text = "PulseRate: ")

      self.DimentionVar = IntVar()
      self.PopulationVar = IntVar()
      self.MinFrequencyVar = StringVar()
      self.MaxFrequencyVar = StringVar()
      self.IteretionVar = IntVar()
      self.AlphaVar = StringVar()
      self.GamaVar = StringVar()
      self.LoudnessVar = StringVar()
      self.PulseRateVar = StringVar()

      self.DimentionF = Entry(self,textvariable=self.DimentionVar)
      self.PopulationF = Entry(self,textvariable=self.PopulationVar)
      self.MinFrequencyF = Entry(self,textvariable=self.MinFrequencyVar)
      self.MaxFrequencyF = Entry(self,textvariable=self.MaxFrequencyVar)
      self.IteretionF = Entry(self,textvariable=self.IteretionVar)
      self.AlphaF = Entry(self,textvariable=self.AlphaVar)
      self.GamaF = Entry(self,textvariable=self.GamaVar)
      self.LoudnessF = Entry(self,textvariable=self.LoudnessVar)
      self.PulseRateF = Entry(self,textvariable=self.PulseRateVar)

      self.start = Button(self,text=" Start  ",command=self.move)

      self.start.grid(row = 9, column =1, sticky = W+E+N+S)

      self.DimentionF.grid(row = 0, column = 1,sticky = W+E+N+S )
      self. PopulationF.grid(row = 1, column = 1, sticky = W+E+N+S)
      self.MinFrequencyF.grid(row = 2, column = 1, sticky = W+E+N+S)
      self.MaxFrequencyF.grid(row = 3, column = 1, sticky = W+E+N+S)
      self.IteretionF.grid(row = 4, column = 1, sticky = W+E+N+S)
      self.AlphaF.grid(row = 5, column = 1, sticky = W+E+N+S)
      self.GamaF.grid(row = 6, column = 1, sticky = W+E+N+S)
      self.LoudnessF.grid(row = 7, column = 1, sticky = W+E+N+S)
      self.PulseRateF.grid(row = 8, column = 1, sticky = W+E+N+S)

      self.DimentionLb.grid(row = 0, column = 0,sticky = W+E+N+S )
      self. PopulationLb.grid(row = 1, column = 0, sticky = W+E+N+S)
      self.MinFrequencyLb.grid(row = 2, column = 0, sticky = W+E+N+S)
      self.MaxFrequencyLb.grid(row = 3, column = 0, sticky = W+E+N+S)
      self.IteretionLb.grid(row = 4, column = 0, sticky = W+E+N+S)
      self.AlphaLb.grid(row = 5, column = 0, sticky = W+E+N+S)
      self.GamaLb.grid(row = 6, column = 0, sticky = W+E+N+S)
      self.LoudnessLb.grid(row = 7, column = 0, sticky = W+E+N+S)
      self.PulseRateLb.grid(row = 8, column = 0, sticky = W+E+N+S)

      self.DimentionVar.set(2)
      self.PopulationVar.set(40)
      self.MinFrequencyVar.set(0.0)
      self.MaxFrequencyVar.set(2.0)
      self.IteretionVar.set(1000)
      self.AlphaVar.set(0.9)
      self.GamaVar.set(0.9)
      self.LoudnessVar.set(0.5)
      self.PulseRateVar.set(0.8)

      self.rowconfigure(0,weight =1)
      self.rowconfigure(1,weight =1)
      self.rowconfigure(2,weight =1)
      self.rowconfigure(3,weight =1)
      self.rowconfigure(4,weight =1)
      self.rowconfigure(5,weight =1)
      self.rowconfigure(6,weight =1)
      self.rowconfigure(7,weight =1)
      self.rowconfigure(8,weight =1)
      self.rowconfigure(9,weight =1)

      self.columnconfigure(0,weight = 1)
      self.columnconfigure(1,weight = 1)
    
   def move(self):
      if(self.ValidationFields()):
         Algorithm = BatAlgorithm(self.DimentionVar.get(), self.PopulationVar.get(), self.IteretionVar.get(),float(self.MinFrequencyVar.get()), float(self.MaxFrequencyVar.get()),float(self.AlphaVar.get()),float(self.GamaVar.get()),float(self.LoudnessVar.get()),float(self.PulseRateVar.get()),self.Rosenbrock)
         Algorithm.move_bat()
      else:
         messagebox.showinfo("Exception", "Введіть, будь ласка, всі поля")


   def Rosenbrock(self,Dim, sol):
   	npSol = np.array(sol)
   	return sum(100*(npSol[1:] - npSol[:-1]**2)**2 + (1 - npSol[:-1])**2)

   def ValidationFields(self):
      if(len(str(self.DimentionVar.get())) == 0):
         return False
      elif (len(str(self.PopulationVar.get())) == 0):
         return False
      elif (len(self.MinFrequencyVar.get()) == 0):
         return False
      elif (len(self.MaxFrequencyVar.get()) == 0):
         return False
      elif (len(str(self.IteretionVar.get())) == 0):
         return False
      elif (len(self.AlphaVar.get()) == 0):
         return False
      elif (len(self.GamaVar.get()) == 0):
         return False
      elif (len(self.LoudnessVar.get()) == 0):
         return False
      elif (len(self.PulseRateVar.get()) == 0):
         return False
      else: return True


def main():
   Gui().mainloop()   

if __name__ == "__main__":
   main()
