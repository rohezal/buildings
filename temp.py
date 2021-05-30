# -*- coding: utf-8 -*-

import csv
import sys
import statistics
import ephem
import datetime
import time
from ephem import cities

import BuildingFeatures
from BuildingFeatures import FeatureData
from BuildingFeatures import SunAndCalendarData


datalist = [] #list of csv with calculated future


#==================================helperfunctions===============================================	

def median_for_lists(input):
	returnlist = []

	for element in input:
		returnlist.append(statistics.median(element))

	return returnlist

def lower_median_for_lists(medianlist, offset = None):
	if(offset == None):
		offset = int(len(medianlist)/50)

	returnlist = []
	for element in medianlist:
		temp = element.copy()
		temp.sort()
		returnlist.append(temp[offset])
	return returnlist

def upper_median_for_lists(medianlist, offset = None):
	if(offset == None):
		offset = 1+int(len(medianlist)/50)
	else:
		offset = offset+1		
		  
		
	returnlist = []
	for element in medianlist:
		temp = element.copy()
		temp.sort()
		#print (temp)
		returnlist.append(temp[-offset])
	return returnlist


def average_for_lists(input):
	returnlist = []

	for element in input:
		returnlist.append(average(element))

	return returnlist		

def average(input):
	sum = 0.0
	for element in input:
		sum = sum + element
	sum = sum / len(input)		
	return sum


	
def loadCSVDataAndFillCaches(csv_reader):
	lastdate = "" 
	for row in csv_reader:
		row[0] = row[0].replace("\"", "")
		datalist.append(FeatureData(row))
		newdate = row[0].split()[0]
				
		if(newdate != lastdate):
			isTheSunShining(newdate,"0:00")
			lastdate = newdate
			#print (newdate)
			

	for datapoint in datalist:
		datapoint.calculateIfSunIsShining()


		
	
def isTheSunShining(mydate, mytime):
	#braunschweig = ephem.Observer()
	#braunschweig.date = mydate
	#braunschweig.lat = '52.155738'
	#braunschweig.lon = '10.313623'
	#braunschweig.elevation=75
	braunschweig = ephem.cities.city("Berlin")
	
	floatime_rise = braunschweig.next_rising(ephem.Sun())
	floatime_set = braunschweig.next_setting(ephem.Sun())
	
	
	edate = ephem.Date(floatime_rise)
	edate_set = ephem.Date(floatime_set)
	sunrise = (edate.datetime() + datetime.timedelta(hours=timezone_delta)).time()
	sunset = (edate_set.datetime() + datetime.timedelta(hours=timezone_delta)).time()
	
	giventime = datetime.datetime.strptime(mytime, '%H:%M').time()
	
	SunAndCalendarData.sunrises[mydate] = sunrise
	SunAndCalendarData.sunsets[mydate] = sunset
	
   
	if giventime > sunrise and giventime < sunset:
		return True
	else:
		return False
	
	
def temperature_test():
	with open('converted_BRICS.csv') as csv_file_brics:	
		csv_reader_brics = csv.reader(csv_file_brics, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
		loadCSVDataAndFillCaches(csv_reader_brics)
		FeatureData.calculateFeatures(datalist)
	
	with open('yearly.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		counter = 0
		
		temp_germany = []
		
		for row in csv_reader:
			if counter == 0:
				#print(row[-1])
				counter = counter + 1
				continue
			#print (row[-1])
			temp_germany.append(float(row[-1]))
		
		temp_germany.sort()
		offset = int(len(temp_germany)/50)
		
		avg = average(temp_germany)		
		med = statistics.median(temp_germany)
		med_lower = temp_germany[offset]
		med_upper = temp_germany[-offset]
		
		avg2median = avg/med
		max2min = med_upper/med_lower
		med2max = med / med_upper
		med2min = med / med_lower
		max_minus_min = abs(med_upper-med_lower)
		
		print(temp_germany)
		print(avg)
		print(med)
		print(med_lower)
		print(med_upper)
		
		print(avg2median)
		print(max2min)
		print(med2max)
		print(med2min)
		print(max_minus_min)
		
		#isTheSunShining("2012/1/1", "07:30")
		print("======================================================")
		print(isTheSunShining("2020/3/12", "4:30"))
		print(isTheSunShining("2020/3/12", "7:30"))
		print(isTheSunShining("2020/3/12", "20:30"))
		print(isTheSunShining("2012/1/1", "7:30"))
		print(isTheSunShining("2012/1/1", "6:20"))
		
		print("======================================================")
	
		print(FeatureData.cachedIsTheSunShining("2020/3/12", "4:30"))
		print(FeatureData.cachedIsTheSunShining("2020/3/12", "7:30"))
		print(FeatureData.cachedIsTheSunShining("2020/3/12", "20:30"))
	
		print(str(SunAndCalendarData.sunrises["2020/3/12"]) + " " + str(SunAndCalendarData.sunsets["2020/3/12"]))
		
		print("======================================================")
		SunAndCalendarData.sunrises['big'] = datetime.datetime.strptime("8:00", '%H:%M').time()
		SunAndCalendarData.sunrises['small'] = datetime.datetime.strptime("7:00", '%H:%M').time()
		print("Test")
		print(SunAndCalendarData.sunrises["2012/1/1"] < SunAndCalendarData.sunrises['big'] )
		print(SunAndCalendarData.sunrises["2012/1/1"] < SunAndCalendarData.sunrises['small'] )

#=================USER ADJUSTABLE PART BEGINN==============================================

timezone_delta = 1 #relative to UTC which is GMT (1 hour before Berlin)

number_of_arguments = len(sys.argv)
if(number_of_arguments == 2):
	filename = sys.argv[1]
	
else:
	print("usage: main.py name_of_the_file.csv. Using now converted_BRICS.csv as a default file")
	filename = 'converted_BRICS.csv'
	
with open(filename) as csv_file_brics:	
	csv_reader_brics = csv.reader(csv_file_brics, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
	loadCSVDataAndFillCaches(csv_reader_brics)
	FeatureData.calculateFeatures(datalist)
	print("starting exporter")
	start = time.time()
	FeatureData.exportToCSV(datalist)
	end = time.time()
	print("exporter time " + "%.2f" % (end-start) + " seconds")
	
	print("starting cached exporter")
	start = time.time()
	#FeatureData.exportToCSVCached(datalist)
	end = time.time()
	print("cached exporter time " + "%.2f" % (end-start) + " seconds")
	
#=================USER ADJUSTABLE PART END==============================================
