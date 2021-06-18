# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""

import csv
import sys
import os
import functools

feature_names = ["date", "time", "original_value", "season", "week_of_year", "quarter_of_year", "day_of_week", "month", "day", "hour", "daylight_saving_time", "sunIsShining", "heating_period", "median_for_a_day", "median_for_a_day_sunup", "median_for_a_day_sundown", "average_for_a_day", "average_for_a_day_sunup", "average_for_a_day_sundown", "median_minus_average_day", "median_minus_average_sunup", "median_minus_average_sundown", "median_to_average_day", "median_to_average_sunup", "median_to_average_sundown", "median_max_value_day", "median_min_value_day", "avg_max_value_day", "avg_min_value_day", "median_max_value_sunup", "median_min_value_sunup", "median_max_value_sundown", "median_min_value_sundown", "avg_max_value_sunup", "avg_min_value_sunup", "avg_max_value_sundown", "avg_min_value_sundown", "median_sunup_minus_sundown", "median_minus_sundown", "median_minus_sunup", "median_sunup_to_sundown", "median_to_sundown", "median_to_sunup", "average_sunup_minus_sundown", "average_minus_sundown", "average_minus_sunup", "average_sunup_to_sundown", "average_to_sundown", "average_to_sunup", "median_max_minus_min_day", "median_max_minus_min_sunup", "median_max_minus_min_sundown", "median_max_to_min_day", "median_max_to_min_sunup", "median_max_to_min_sundown", "avg_max_minus_min_day", "avg_max_minus_min_sunup", "avg_max_minus_min_sundown", "avg_max_to_min_day", "avg_max_to_min_sunup", "avg_max_to_min_sundown", "variance_day", "variance_sunup", "variance_sundown"]

def number_to_feature(number):
	return feature_names[number];
	
	

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

with open(path+"/"+files[0], newline='', encoding='ISO-8859-1') as csvfile:
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
with open(sourcefile, newline='', encoding='ISO-8859-1') as csvfile:
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
		headers[-1][1].append(id + "_" + number_to_feature(i)) 

	headers[-1].append([]) #ids IGS_BRICS_3210 ISP01 LA0
	skip_first = False
	for element in sinfos:
		if(skip_first == False):
			skip_first = True
			headers[-1][2].append(element)
			continue
		headers[-1][2].append(element + "_" + number_to_feature(i)) 		
		
	headers[-1].append(original_header[3]) #long info
	headers[-1].append(original_header[4]) #minimum
	headers[-1].append(original_header[5]) #maximum
	headers[-1].append(original_header[6]) #unit
	
print(len(ram_csv_files))	

counter = 0
for file in files:
	with open(path+"/"+file, newline='', encoding='ISO-8859-1') as csvfile:
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
	
	if(counter == 0 or counter == 1 or counter == 2): #remove time, date and original data point from the feature files
		counter = counter+1		   
		continue
	
	with open("converted_results/"+sourcefile.split(".")[0]+"_"+number_to_feature(counter)+".csv", "w", encoding='ISO-8859-1') as resultFile:
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

