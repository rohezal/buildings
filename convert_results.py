# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""

import csv
import sys
import os
import functools

def compare(item1, item2):
	
	number1 = 0
	number2 = 0
	
	if(item1[1] == '_'):
		number1 = int(item1[0]) 

	else:
		number1 = int(item1[0])*10+int(item1[1])

	if(item2[1] == '_'):
		number2 = int(item2[0]) 

	else:
		number2 = int(item2[0])*10+int(item2[1])

	if number1 < number2:
		return -1
	elif number1 > number2:
		return 1
	else:
		return 0

if(len(sys.argv) != 2):
	print("Usage: convert_results.py foldername")
	sys.exit(1)

path = sys.argv[1]
files = os.listdir(path) # returns list	
#files.sort(key=compare)
files = sorted(files,key=functools.cmp_to_key(compare))

number_of_files = len(files)
ram_csv_files = []

number_of_features = 0

with open(path+"/"+files[0], newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=';', quotechar='|')
	for row in reader:
		number_of_features = len(row)
		break
csvfile.close()	

for i in range(number_of_features):
	ram_csv_files.append([])
	
print(len(ram_csv_files))	

counter = 0
for file in files:
	with open(path+"/"+file, newline='') as csvfile:
		print(file)								
		reader = csv.reader(csvfile, delimiter=';', quotechar='|')

		rowcounter = 0
		for row in reader:
			if(counter == 0): # create a new list for each row of a feature
				for ram_csv in ram_csv_files:
					ram_csv.append([])
		
			featurecounter = 0
			for element in row:
				ram_csv_files[featurecounter][rowcounter].append(element)
				featurecounter += 1
				#if(rowcounter > 2):
					#rowcounter = rowcounter+1
					#continue
			rowcounter += 1				
			#ram_csv_files[counter].append(rowlist)				

	csvfile.close()
	counter += 1
	

	
counter = 0	
for file in ram_csv_files:
	with open("converted_results/"+str(counter)+".csv", "w") as resultFile:
		wr = csv.writer(resultFile)
		wr.writerows(ram_csv_files[counter])
		#for row in ram_csv_files[counter]:
			 #wr.writerow(row)  
			 #print(row)
	counter = counter+1		   
	resultFile.close()		   
	
	#for row in reader:
	#	print(row)

