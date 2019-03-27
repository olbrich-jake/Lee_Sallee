#Python Script for Lee Sallee Spatial Corresponance metric for two simulated fires
#Two loops were created for distinguishing the two fires, area intersected is divided 
  #by area contained between both historical and simulation
#For personal use, adjustments need to me made for name and area being compared.
#This code has historical area written out rather than derived. 
#File name is formated as "Sim_" + "Distinguishing simulation name (i.e 'Fam' or 'RE')" + "filter" + "simulation iteration" + ".shp"
#Output is a text file with columns: Fire_name, Actual_Fire, SIM_FIRE, Int_Fire, Union_Fire
  #Fire_Name is the file name
  #Actual_fire: is the area of the historical fire
  #SIM_FIRE: is the area of the simulated fire
  #Int_Fire: Area of the actual and simulated fires after intersection
  #Union_Fire: Area of the actual and simulated fires after union
