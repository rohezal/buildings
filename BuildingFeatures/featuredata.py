#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:57:48 2020

@author: rohezal
"""

import csv
import statistics
import ephem
import datetime
from ephem import cities
from . import featurecalculation
from . import valuecontainer
from .valuecontainer import ValueContainer


INITVALUE = -666999 #if you see this value somewhere it is most likely an uninitalized variable

class SunAndCalendarData:
	sunrises = {} #dictonary to lookup when the sun rises
	sunsets = {} #dictonary to lookup when the sun sets
	heating_period_start_month=8 #start the heating AFTER august
	heating_period_end_month=5 #end the heating BEFORE may
	
	def clearCaches():
		SunAndCalendarData.sunrises = {} #dictonary to lookup when the sun rises
		SunAndCalendarData.sunsets = {} #dictonary to lookup when the sun sets


class FeatureData:
	dayValues = ValueContainer()

	def __init__(self, data):
		#datestring = data[0].replace("\"", "") #take the first row and assume it is date and time. e.g. 1.1.2020 19:30 
		datestring = data[0] #take the first row and assume it is date and time. e.g. 1.1.2020 19:30 
		self.date = datestring.split()[0] #split the date part. 1.1.2020 19:30 -> 1.1.2020
		self.time = datestring.split()[1] #split the time part. 1.1.2020 19:30 -> 19:30
		self.rowdata = data[1:] #take each row after the first one, since the first one is date and time
		self.sunIsShining=False #will be calculated by calculateIfSunIsShining in loadCSVDataAndFillCaches
		self.month=int(self.date.split(".")[1]) #13.5.2020 -> 5
		self.heating_period = FeatureData.dateToMonth(self.date) #if month bigger than september or less than may?

		self.outside_temperature=INITVALUE
		
		self.day_median=[]
		self.sunup_median=[]
		self.sundown_median=[]
		self.median_sunup_minus_sundown=[]
		self.median_sunup_to_sundown=[]
		self.day_median_to_sunup=[]
		self.day_median_to_down=[]
		self.day_median_minus_down=[]
		self.day_median_minus_sunup=[]
		self.day_avg = []
		self.sunup_avg= []
		self.sundown_avg= []
		self.avg_sunup_minus_sundown= []
		self.avg_minus_sunup= []
		self.avg_minus_sundown= []
		
	def calculateIfSunIsShining(self):
		self.sunIsShining=FeatureData.cachedIsTheSunShining(self.date, self.time)
		#self.sunIsShining=isTheSunShining(self.date, self.time)
		
	def clearCaches():
		FeatureData.dayValues = ValueContainer()
		SunAndCalendarData.clearCaches();

		
	def calculateFeatures(datapoints):
		currentdate = datapoints[0].date
		day_buffer_list = []
		day_buffer_sunrise_list = []
		day_buffer_sunset_list = []

		for i in range(len(datapoints)):
			if (currentdate != datapoints[i].date):
				FeatureData.helperCalculateFeatures(currentdate, day_buffer_list,day_buffer_sunrise_list,day_buffer_sunset_list)
				day_buffer_list.clear()
				day_buffer_sunrise_list.clear()
				day_buffer_sunset_list.clear()
				currentdate = datapoints[i].date
				#print (currentdate)

			day_buffer_list.append(datapoints[i].rowdata)
			if(datapoints[i].sunIsShining == True):
				day_buffer_sunrise_list.append(datapoints[i].rowdata)
			else:
				day_buffer_sunset_list.append(datapoints[i].rowdata)
			  
		
	def helperCalculateFeatures(date, day_buffer_list,day_buffer_sunup_list,day_buffer_sundown_list):
		
		#we have the data in this format t_in, t_out, p_in,p_out per datapoint. now we need the value for all datapoints of a day
		number_of_values_per_row =len(day_buffer_list[0]) #the number of different values per row is the same
		day_features = []
		sunup_features = []
		sundown_features = []
		
		for i in range(number_of_values_per_row):
			day_features.append([]) #add a list for each column
			sunup_features.append([]) #add a list for each column
			sundown_features.append([]) #add a list for each column
			
		for row in day_buffer_list:
			for i in range(len(row)):
				day_features[i].append(row[i])

		for row in day_buffer_sunup_list:
			for i in range(len(row)):
				sunup_features[i].append(row[i])

		for row in day_buffer_sundown_list:
			for i in range(len(row)):
				sundown_features[i].append(row[i])
				
		FeatureData.dayValues.median_for_a_day[date] = featurecalculation.median_for_lists(day_features)
		FeatureData.dayValues.median_for_a_day_sunup[date] = featurecalculation.median_for_lists(sunup_features)
		FeatureData.dayValues.median_for_a_day_sundown[date] = featurecalculation.median_for_lists(sundown_features)
		
		FeatureData.dayValues.average_for_a_day[date] = featurecalculation.average_for_lists(day_features)
		FeatureData.dayValues.average_for_a_day_sunup[date] = featurecalculation.average_for_lists(sunup_features)
		FeatureData.dayValues.average_for_a_day_sundown[date] = featurecalculation.average_for_lists(sundown_features)
		
		FeatureData.dayValues.median_max_value_day[date] = featurecalculation.upper_median_for_lists(day_features)
		FeatureData.dayValues.median_min_value_day[date] = featurecalculation.lower_median_for_lists(day_features)

		FeatureData.dayValues.avg_max_value_day[date] = featurecalculation.upper_average_list(day_features)
		FeatureData.dayValues.avg_min_value_day[date] = featurecalculation.lower_average_list(day_features)
		
		FeatureData.dayValues.median_max_value_sunup[date] = featurecalculation.upper_median_for_lists(sunup_features)
		FeatureData.dayValues.median_min_value_sunup[date] = featurecalculation.lower_median_for_lists(sunup_features)
		FeatureData.dayValues.median_max_value_sundown[date] = featurecalculation.upper_median_for_lists(sundown_features)
		FeatureData.dayValues.median_min_value_sundown[date] = featurecalculation.lower_median_for_lists(sundown_features)
		
		FeatureData.dayValues.avg_max_value_sunup[date] = featurecalculation.upper_average_list(sunup_features)
		FeatureData.dayValues.avg_min_value_sunup[date] = featurecalculation.lower_average_list(sunup_features)
		FeatureData.dayValues.avg_max_value_sundown[date] = featurecalculation.upper_average_list(sundown_features)
		FeatureData.dayValues.avg_min_value_sundown[date] = featurecalculation.lower_average_list(sundown_features)
	
		#print(day_buffer_list);
		
	def dateToMonth(date):
		month = "undefined: " + date
		assert date.count(".") == 2
		month = date.split(".")[1] #split 30.1.2020 to 20 1 2020, keep the 1
		
		return month
	
	def dateToDayOfWeek(date):
		day = date
		#ans = datetime.date(year, month, day)

		return day	
	
	def dateToIsHeatingPeriod(date):
		month = "undefined: " + date
		assert date.count(".") == 2
		month = date.split(".")[1] #split 30.1.2020 to 20 1 2020, keep the 1
		month_int = int(month)
		
		return month_int > SunAndCalendarData.heating_period_start_month and month_int < SunAndCalendarData.heating_period_end_month #heating is required between october and the first of may
		
	
	def dateToYear(date):
		year = "undefined"
		assert date.count(".") == 2
		year = date.split(".")[2] #split 30.1.2020 to 30 1 2020, keep the 2020
		return year
		
	def dateToQuarter(date):
		month = "undefined: " + date
		assert date.count(".") == 2
		month = date.split(".")[1] #split 30.1.2020 to 20 1 2020, keep the 1
		quarter = int(month)/4+1
		return quarter
		
	def dateToIsWeekend(date):
		date=date

	def timeToHourOfDay(time):		
		hour = time
		
	def getLastSundayOfMonth(date):
		return 0
		
	def dateToDayOfMonth(date):
		return date
	
	def dateToWeekOfYear(date):
		return date
		
	def isSummerTime(date):		
		month = FeatureData.dateToMonth(date)
		dayOfMonth = FeatureData.dateToDayOfMonth(date)
		dayOfWeek = FeatureData.dateToDayOfWeek(date)
		
		if(month > 2 and month < 11):
			if(month > 3 and month < 10): #April to September
				return True
			elif (month == 2):
				return dayOfMonth >= FeatureData.getLastSundayOfMonth(date)
				
			elif (month == 10):
				return dayOfMonth < FeatureData.getLastSundayOfMonth(date)
		
		return False
		
		
		
		
		
	def copyFeaturesFromDictonaryToFeatureData(datapoints):
		for point in datapoints:
			point.day_median = FeatureData.dayValues.median_for_a_day[point.date]
		
		
	def exportToCSV(datapoints):
		print("implement me")
		
	def cachedIsTheSunShining(mydate, mytime):
		giventime = datetime.datetime.strptime(mytime, '%H:%M').time()

		if giventime > SunAndCalendarData.sunrises[mydate] and giventime < SunAndCalendarData.sunsets[mydate]:
			return True
		else:
			return False		