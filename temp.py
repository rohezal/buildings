# -*- coding: utf-8 -*-

import csv
import statistics
import ephem
import datetime
from ephem import cities
#import featurecalculation
#import featuredata

import BuildingFeatures
from BuildingFeatures import FeatureData
from BuildingFeatures import SunAndCalendarData

#from BuildingFeatures import featuredata 
#from BuildingFeatures import SunAndCalendarData 
#from BuildingFeatures import FeatureData

datalist = [] #list of csv with calculated future
timezone_delta = 1 #relative to UTC which is GMT (1 hour before Berlin)


class ValueContainer:
	def __init__(self):
		#medians
		self.median_for_a_day = {}
		self.median_for_a_day_sunup= {}
		self.median_for_a_day_sundown= {}
		
		#averages
		self.average_for_a_day = {}
		self.average_for_a_day_sunup= {}
		self.average_for_a_day_sundown= {}
		
		#median spread and relations
		self.median_sunup_minus_sundown={}
		self.median_minus_sundown={}
		self.median_minus_sunup={}

		self.median_sunup_to_sundown={}
		self.median_to_sundown={}
		self.median_to_sunup={}

		#average spread and relations
		self.average_sunup_minus_sundown={}
		self.average_minus_sundown={}
		self.average_minus_sunup={}

		self.average_sunup_to_sundown={}
		self.average_to_sundown={}
		self.average_to_sunup={}  
		
		#max and min values of the lowest the outer 5% median method
		self.median_max_value_day = {}
		self.median_min_value_day = {}
		self.median_max_value_sunup = {}
		self.median_min_value_sunup = {}
		self.median_max_value_sundown = {}
		self.median_min_value_sundown = {}
		
		
		#max and min values of the lowest the outer 5% average method
		self.avg_max_value_day = {}
		self.avg_min_value_day = {}
		self.avg_max_value_sunup = {}
		self.avg_min_value_sunup = {}
		self.avg_max_value_sundown = {}
		self.avg_min_value_sundown = {}

		#spread of min and max median
		self.median_max_minus_min_day = {}
		self.median_max_minus_min_sunup = {}
		self.median_max_minus_min_sundown = {}
		
		self.median_max_to_min_day = {}
		self.median_max_to_min_sunup = {}
		self.median_max_to_min_sundown = {}


		#spread of max and min average
		self.avg_max_minus_min_day = {}
		self.avg_max_minus_min_sunup = {}
		self.avg_max_minus_min_sundown = {}

		self.avg_max_to_min_day = {}
		self.avg_max_to_min_sunup = {}
		self.avg_max_to_min_sundown = {}
		
		
		
		def calculateFeaturesFromMediaAndAverage(self):
			for key in self.median_for_a_day.key():
				self.median_sunup_minus_sundown[key] = self.list_minus_list(self.median_for_a_day_sunup[key],self.median_for_a_day_sundown[key])
				self.median_minus_sunup[key] = self.list_minus_list(self.median_for_a_day[key],self.median_for_a_day_sunup[key])
				self.median_minus_sundown[key] = self.list_minus_list(self.median_for_a_day[key],self.median_for_a_day_sundown[key])
				
				self.median_sunup_to_sundown[key] = self.list_divided_by_list(self.median_for_a_day_sunup[key],self.median_for_a_day_sundown[key])
				self.median_to_sunup[key] = self.list_divided_by_list(self.median_for_a_day[key],self.median_for_a_day_sunup[key])
				self.median_to_sundown[key] = self.list_divided_by_list(self.median_for_a_day[key],self.median_for_a_day_sundown[key])
				
				self.average_sunup_minus_sundown[key] = self.list_minus_list(self.average_for_a_day_sunup[key],self.average_for_a_day_sundown[key])
				self.average_minus_sunup[key] = self.list_minus_list(self.average_for_a_day[key],self.average_for_a_day_sunup[key])
				self.average_minus_sundown[key] = self.list_minus_list(self.average_for_a_day[key],self.average_for_a_day_sundown[key])
				
				self.average_sunup_to_sundown[key] = self.list_divided_by_list(self.average_for_a_day_sunup[key],self.average_for_a_day_sundown[key])
				self.average_to_sunup[key] = self.list_divided_by_list(self.average_for_a_day[key],self.average_for_a_day_sunup[key])
				self.average_to_sundown[key] = self.list_divided_by_list(self.average_for_a_day[key],self.average_for_a_day_sundown[key])
	
				#extreme values				
				self.median_max_minus_min_day = self.list_minus_list(self.median_max_value_day[key],self.median_min_value_day[key])
				self.median_max_minus_min_sunup = self.list_minus_list(self.median_max_value_sunup[key],self.median_min_value_sunup[key])
				self.median_max_minus_min_sundown = self.list_minus_list(self.median_max_value_sundown[key],self.median_min_value_sundown[key])

				self.avg_max_minus_min_day = self.list_minus_list(self.avg_max_value_day[key],self.avg_max_value_day[key])
				self.avg_max_minus_min_sunup = self.list_minus_list(self.avg_max_value_sunup[key],self.avg_max_value_sunup[key])
				self.avg_max_minus_min_sundown = self.list_minus_list(self.avg_max_value_sundown[key],self.avg_max_value_sundown[key])
				
				self.median_max_to_min_day = self.list_divided_by_list(self.median_max_value_day[key],self.median_min_value_day[key])
				self.median_max_to_min_sunup = self.list_divided_by_list(self.median_max_value_sunup[key],self.median_min_value_sunup[key])
				self.median_max_to_min_sundown = self.list_divided_by_list(self.median_max_value_sundown[key],self.median_min_value_sundown[key])

				self.avg_max_to_min_day = self.list_divided_by_list(self.avg_max_value_day[key],self.avg_max_value_day[key])
				self.avg_max_to_min_sunup = self.list_divided_by_list(self.avg_max_value_sunup[key],self.avg_max_value_sunup[key])
				self.avg_max_to_min_sundown = self.list_divided_by_list(self.avg_max_value_sundown[key],self.avg_max_value_sundown[key])
		

				
		def list_minus_list(list1, list2):
			newlist = []
			for i in range(len(list1)):
				newlist.append(list1[i]-list[2])
			return newlist				
		
		def list_divided_by_list(list1,list2):
			newlist = []
			for i in range(len(list1)):
				newlist.append(list1[i]/list[2])
			return newlist				
			
			
			
		
#def loadCSVAndComputeSunrise(filename):

#def calculateFeatures(datapoints):
	
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
	
	


#featurecalculation.unit_test()

	
with open('converted_BRICS.csv') as csv_file_brics:	
	csv_reader_brics = csv.reader(csv_file_brics, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
	#csv_reader_brics = pandas.read_csv(csv_file_brics, delimiter=",", decimal=",")

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
	
	
	
	
	