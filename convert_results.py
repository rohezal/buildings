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

if(len(sys.argv) != 3):
	print("Usage: convert_results.py foldername sourcefile")
	sys.exit(1)

path = sys.argv[1]
sourcefile = sys.argv[2]
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

#create an extra csv file for each feature
for i in range(number_of_features):
	ram_csv_files.append([])



#read in the header
original_header = []
with open(sourcefile, newline='') as csvfile:
	line_reader_counter = 0
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		original_header.append([])
		for element in row:
			original_header[-1].append(element)
		line_reader_counter = line_reader_counter+1
		if(line_reader_counter > 6):
			break
csvfile.close()		


headers = []	
ids = []
sinfos = [] # short infos

for element in original_header[1]:
	ids.append(element)
	
for element in original_header[2]:
	sinfos.append(element)	
	

	
for i in range(number_of_features):
	headers.append([])
	headers[-1].append(original_header[0]) #record software  synavision CSV format 2.0 DE - encoding: ISO-8859-1
	skip_first = False
	headers[-1].append([]) #ids IGS_BRICS_3210 ISP01 LA0
	for id in ids:
		if(skip_first == False):
			skip_first = True
			headers[-1][1].append(id)
			continue
		headers[-1][1].append(id + "_feature" + str(i)) 

	headers[-1].append([]) #ids IGS_BRICS_3210 ISP01 LA0
	skip_first = False
	for element in sinfos:
		if(skip_first == False):
			skip_first = True
			headers[-1][2].append(element)
			continue
		headers[-1][2].append(element + "_feature" + str(i)) 		
		
	headers[-1].append(original_header[3]) #long info
	headers[-1].append(original_header[4]) #minimum
	headers[-1].append(original_header[5]) #maximum
	headers[-1].append(original_header[6]) #unit
	
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
					ram_csv[-1].append(row[0] + " " + row[1] )
		
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
	with open("converted_results/"+sourcefile.split(".")[0]+"_feature"+str(counter)+".csv", "w") as resultFile:
		wr = csv.writer(resultFile)
		wr.writerows(headers[counter])
		wr.writerows(ram_csv_files[counter])
		#for row in ram_csv_files[counter]:
			 #wr.writerow(row)  
			 #print(row)
	counter = counter+1		   
	resultFile.close()		   
	
	#for row in reader:
	#	print(row)

