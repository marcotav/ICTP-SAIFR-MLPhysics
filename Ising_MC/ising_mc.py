# Monte Carlo for the Ising model

import numpy as np
import random

#input parameters:
J = 1 #coupling parameter
L = 4 #linear size of the lattice
N_spins = L**2 #total number of spins

# temperature list:
#T_list=[1.0000000000000000,1.0634592657106510,1.1269185314213019,1.1903777971319529,1.2538370628426039,1.3172963285532548,1.3807555942639058,1.4442148599745568,1.5076741256852078,1.5711333913958587,1.6345926571065097,1.6980519228171607,1.7615111885278116,1.8249704542384626,1.8884297199491136,1.9518889856597645,2.0153482513704155,2.0788075170810667,2.1422667827917179,2.2057260485023691,2.3326445799236715,2.3961038456343227,2.4595631113449739,2.5230223770556250,2.5864816427662762,2.6499409084769274,2.7134001741875786,2.7768594398982298,2.8403187056088810,2.9037779713195322,2.9672372370301834,3.0306965027408346,3.0941557684514858,3.1576150341621370,3.2210742998727881,3.2845335655834393,3.3479928312940905,3.4114520970047417,3.4749113627153929,3.5383706284260401]
T_list = [4.0, 3.0, 2.0]

initialState = 0 #0 means start from all up state, 1 means start from random state

n_warmupSweeps = 10
n_bins = 10
n_sweepsPerBin=5

def getEnergy():
  currEnergy = 0
  for i in range(N_spins):
    currEnergy += -J*( spins[i]*spins[neighbours[i,0]] + spins[i]*spins[neighbours[i,1]] )
  return currEnergy

def sweep():
  #do one sweep (N_spins local updates):
  for i in range(N_spins):
    #randomly choose which spin to consider flipping:
    site = random.randint(0,N_spins-1)
      
    deltaE = 0
    #calculate the change in energy of the proposed move by considering only the nearest neighbours:
    for j in range(4):
      deltaE += 2*J*spins[site]*spins[neighbours[site,j]]
  
    if (deltaE <= 0) or (random.random() < np.exp(-deltaE/T)):
      #flip the spin:
      spins[site] = -spins[site]
  #end loop over i


neighbours = np.zeros((N_spins,4),dtype=np.int)
#fill in the neighbours array (using periodic boundary conditions):
for i in range(N_spins):
  #neighbour to the right:
  neighbours[i,0]=i+1
  if i%L==(L-1):
    neighbours[i,0]=i+1-L
  
  #upwards neighbour:
  neighbours[i,1]=i+L
  if i >= (N_spins-L):
    neighbours[i,1]=i+L-N_spins

  #neighbour to the left:
  neighbours[i,2]=i-1
  if i%L==0:
    neighbours[i,2]=i-1+L

  #downwards neighbour:
  neighbours[i,3]=i-L
  if i <= (L-1):
    neighbours[i,3]=i-L+N_spins
#end of for loop

#initially, the spins are all up (a low-T phase) or all random (a high-T phase):
spins = np.ones(N_spins,dtype=np.int)
if initialState != 0:
  for i in range(N_spins):
    spins[i] = 2*random.randint(0,1) - 1 #either +1 or -1

#loop over all temperatures:
for T in T_list:
  print "*** T = %f ***" %T
  
  #warm-up sweeps:
  for i in range(n_warmupSweeps):
    sweep()

  #start doing measurements:
  aveEnergy = 0
  for i in range(n_bins):
    for j in range(n_sweepsPerBin):
      sweep()
    #end loop over j
    aveEnergy += getEnergy()
  #end loop over i


#end loop over temperature