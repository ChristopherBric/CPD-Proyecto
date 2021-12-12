#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

file_in = "RngStream.cpp funclass.cpp RngStreamSupp.cpp driverLTM_mpi_mod.cpp"
file_out = "mpi_ltm"
file_time = "ResultTime"
max_np = 6
max_ntest = 10

date = datetime.now().strftime('%d-%m-%Y')
hour = datetime.now().strftime('%H-%M-%S')
file_time = (file_time+'_'+date+'_'+hour+".txt")

print("Compiling MPI Files ...		",end="",flush=True)
print("[WAIT]",end='\r')
os.system("mpic++ " + file_in + " -o " + file_out)
print("Compiling MPI Files ...          ",end="",flush=True)
print("[DONE]\n")
print("Tests Per Process: "+str(max_ntest)+"\n")
print("Starting ...\n")

file2 = open (file_time,"a")
file2.write("np,time,speedup,effiency\n")
file2.close()


for numX in range(max_np):
	np = str(numX + 1)
	Sum = 0

	for numY in range(max_ntest):
		print("Test With " + np + " Processes ...         ",end="",flush=True)
		print("[" + str(numY+1) + "]",end='\r')
		os.system("mpirun -np " + np + " ./" + file_out + "> temp.txt")
		file1 = open("temp.txt","r+")
		file1.seek(0)
		Sum += float(file1.readline())
		file1.close()

	time = Sum/max_ntest
	if numX == 0:
		Sec=time
	speed = Sec/time
	efic = speed/(numX+1)

	print("Test With " + np + " Processes ...         ",end="",flush=True)
	print("[DONE]",end='\n')

	print("Tiempo: ",end="",flush=True)
	print('{0:.6f}'.format(time),end="",flush=True)
	print(" Speedup: ",end="",flush=True)
	print('{0:.6f}'.format(speed),end="",flush=True)
	print(" Efficiency: ",end="",flush=True)
	print('{0:.6f}'.format(efic),end="\n\n")

	file2 = open (file_time,"a")
	file2.write(np+","+str(time)+","+str(speed)+","+str(efic)+"\n")
	file2.close()

os.system("rm temp.txt")
print("... Finished.")
