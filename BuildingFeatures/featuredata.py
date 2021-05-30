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
	heating_period_start_month=9 #start the heating AFTER september
	heating_period_end_month=4 #end the heating BEFORE may
	CONSTANT_SATURDAY = 6
	CONSTANT_SUNDAY = 7
	
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

		#self.month=int(self.date.split(".")[1]) #13.5.2020 -> 5
		#self.day = int(self.date.split(".")[0]) #13.5.2020 -> 13
		#self.hour = int(self.time.split(":")[0]) #19:30 -> 19
		
		self.month = FeatureData.dateToMonth(self.date) #13.5.2020 -> 5
		self.day = FeatureData.dateToDay(self.date) #13.5.2020 -> 13
		self.hour = FeatureData.timeToHourOfDay(self.time) #19:30 -> 19
		
		self.day_of_week = FeatureData.dateToDayOfWeek(self.date)
		self.week_of_year = FeatureData.dateToWeekOfYear(self.date)
		self.quarter_of_year = FeatureData.dateToQuarter(self.date)
		self.season = FeatureData.dateToSeason(self.date)
		
		self.heating_period = FeatureData.dateToMonth(self.date) #if month bigger than september or less than may?
		self.daylight_saving_time = FeatureData.isDaylightSavingTime(self.date)
		self.outside_temperature=INITVALUE
		
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

			#just used for the last element, can be ignored for all other elements
			if(i == (len(datapoints)-1)):  #go until the last element of list. this is because for the last date currentdate wont change in regard to datapoints and we would miss the last element				
				FeatureData.helperCalculateFeatures(currentdate, day_buffer_list,day_buffer_sunrise_list,day_buffer_sunset_list)
				day_buffer_list.clear()
				day_buffer_sunrise_list.clear()
				day_buffer_sunset_list.clear()
				currentdate = datapoints[i].date
				
		#done with medians / averages. lets calculate the ratios / distances between min max values etc
		FeatureData.dayValues.calculateFeaturesFromMedianAndAverage()
		
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
		
		FeatureData.dayValues.variance_day[date] = featurecalculation.calculateVarianceForTwoDimensionaLists(day_features, FeatureData.dayValues.average_for_a_day[date])
		FeatureData.dayValues.variance_sunup[date] = featurecalculation.calculateVarianceForTwoDimensionaLists(sunup_features, FeatureData.dayValues.average_for_a_day_sunup[date])
		FeatureData.dayValues.variance_sundown[date] = featurecalculation.calculateVarianceForTwoDimensionaLists(sundown_features, FeatureData.dayValues.average_for_a_day_sundown[date])
	
		#print(day_buffer_list);
		
	def dateToMonth(date):
		month = "undefined: " + date
		assert date.count(".") == 2
		month = date.split(".")[1] #split 30.1.2020 to 20 1 2020, keep the 1
		return month
	
	def dateToDay(date):
		day = date
		assert date.count(".") == 2
		day = date.split(".")[0] #split 30.1.2020 to 20 1 2020, keep the 30
		return day
	
	
	def dateToDayOfWeek(date):
		day = date
		#ans = datetime.date(year, month, day)
		year = int(FeatureData.dateToYear(date))
		month = int(FeatureData.dateToMonth(date))
		day = int(FeatureData.dateToDay(date))
		
		return datetime.datetime(year, month, day).isoweekday()
		
	
	def dateToIsHeatingPeriod(date):
		month = "undefined: " + date
		assert date.count(".") == 2
		month = date.split(".")[1] #split 30.1.2020 to 20 1 2020, keep the 1
		month_int = int(month)
		
		return not (month_int > SunAndCalendarData.heating_period_end_month and month_int < SunAndCalendarData.heating_period_start_month) #heating is required between october and the first of may
		
	
	def dateToYear(date):
		year = "undefined"
		assert date.count(".") == 2
		year = date.split(".")[2] #split 30.1.2020 to 30 1 2020, keep the 2020
		return year
		
	def dateToQuarter(date):
		month = "undefined: " + date
		assert date.count(".") == 2
		month = date.split(".")[1] #split 30.1.2020 to 20 1 2020, keep the 1
		quarter = int((int(month)-1)/3)+1
		return quarter
		
	def dateToIsWeekend(date):
		dayOfWeek = FeatureData.dateToDayOfWeek(date)		
		return dayOfWeek == SunAndCalendarData.CONSTANT_SATURDAY or dayOfWeek == SunAndCalendarData.CONSTANT_SUNDAY
	
	def dateToIsSunday(date):
		dayOfWeek = FeatureData.dateToDayOfWeek(date)		
		return dayOfWeek == SunAndCalendarData.CONSTANT_SUNDAY
	
	def dateToSeason(date):
		year = int(FeatureData.dateToYear(date))
		month = int(FeatureData.dateToMonth(date))
		day = int(FeatureData.dateToDay(date))
		
		# get the current day of the year
		doy = datetime.date(year, month, day).timetuple().tm_yday
		
		# "day of year" ranges for the northern hemisphere
		spring = range(80, 172)
		summer = range(172, 264)
		fall = range(264, 355)
		# winter = everything else
		
		if doy in spring:
		  season = 1
		elif doy in summer:
		  season = 2
		elif doy in fall:
		  season = 3
		else:
		  season = 0

		return season
		
	def dateToWeekOfYear(date):
		year = int(FeatureData.dateToYear(date))
		month = int(FeatureData.dateToMonth(date))
		day = int(FeatureData.dateToDay(date))
		
		week_of_year = datetime.date(year, month, day).isocalendar()[1]
		return week_of_year


	def timeToHourOfDay(time):		
		hour = time
		assert hour.count(":") == 1
		hour = hour.split(":")[0] #split 30.1.2020 to 20 1 2020, keep the 1
		return hour
		
	def getLastSundayOfMonth(date):
		year = int(FeatureData.dateToYear(date))
		month = int(FeatureData.dateToMonth(date))
		#day = int(FeatureData.dateToDay(date))
		day = 20

		next_month = month
		mydate = datetime.date(year,month,day)
		last_sunday_saved = "UNDEFINED"
		
		if(FeatureData.dateToIsSunday(date) == True):
			mydate = mydate + datetime.timedelta(days=1)
			next_month =  int(FeatureData.dateToMonth(mydate.strftime("%d.%m.%Y")))
			if(next_month > month):
				return date
				
		
		while month == next_month:
			mydate = mydate + datetime.timedelta(days=1)
			next_month =  int(FeatureData.dateToMonth(mydate.strftime("%d.%m.%Y")))
			my_date_string = mydate.strftime("%d.%m.%Y")
			
			if(month != next_month):
				break
			
			if(FeatureData.dateToIsSunday(my_date_string) == True):
				last_sunday_saved = my_date_string
			
		return last_sunday_saved
		
	def isDaylightSavingTime(date): #summnertime check
		month = int(FeatureData.dateToMonth(date))
		
		if (month == 3 or month == 10):
			day = int(FeatureData.dateToDay(date))
			last_sunday = int(FeatureData.dateToDay(FeatureData.getLastSundayOfMonth(date)))
			
			if(month == 3):
				return day < last_sunday #if day not yet last sunday saving time is still applied
			else: #month == 11
				return day >= last_sunday #if day is last sunday or later saving time started
		else:
			#print(date + ": month < 3:" + str(month < 3) + " | month > 10" + str(month > 10)  )
			saving_time = month < 3 or month > 10 #january, february, november, december: smaller than march bigger than no october
			return saving_time
		
		
		
	def copyFeaturesFromDictonaryToFeatureData(datapoints):
		for point in datapoints:
			point.day_median = FeatureData.dayValues.median_for_a_day[point.date]
		

	def exportToCSVCached(datapoints):
		timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
		csv_cache = []
		number_of_columns = len(datapoints[0].rowdata)
		
		for i in range(number_of_columns):
			csv_cache.append([])

		for point in datapoints:
			for i in range(len(point.rowdata)):
				filename = "results/"+str(timestamp)+"_datapoint_"+str(i)+".csv"
						
				csv_row = []
					
				csv_row.append(point.date)
				csv_row.append(point.time)
				csv_row.append(point.rowdata[i])					
				csv_row.append(point.season)
				csv_row.append(point.week_of_year)
				csv_row.append(point.quarter_of_year)
	
				csv_row.append(point.day_of_week)
				csv_row.append(point.month)
				
				csv_row.append(point.day)
				csv_row.append(point.hour)
				csv_row.append(point.daylight_saving_time)
				csv_row.append(point.sunIsShining)
				csv_row.append(point.heating_period)

				date = point.date
					
				#medians
				csv_row.append(FeatureData.dayValues.median_for_a_day[date][i])
				csv_row.append(FeatureData.dayValues.median_for_a_day_sunup[date][i])
				csv_row.append(FeatureData.dayValues.median_for_a_day_sundown[date][i])
			
				#averages
				csv_row.append(FeatureData.dayValues.average_for_a_day[date][i])
				csv_row.append(FeatureData.dayValues.average_for_a_day_sunup[date][i])
				csv_row.append(FeatureData.dayValues.average_for_a_day_sundown[date][i])

#=======================MEDIAN TO AVERAGE RELATIONS =========================================================								
					
				csv_row.append(FeatureData.dayValues.median_minus_average_day[date][i])
				csv_row.append(FeatureData.dayValues.median_minus_average_sunup[date][i])
				csv_row.append(FeatureData.dayValues.median_minus_average_sundown[date][i])

				csv_row.append(FeatureData.dayValues.median_to_average_day[date][i])
				csv_row.append(FeatureData.dayValues.median_to_average_sunup[date][i])
				csv_row.append(FeatureData.dayValues.median_to_average_sundown[date][i])
					
		
#=======================MIN/MAX VALUES AUF MEDIANS/AVGS=========================================================			
			
				#max and min values of the lowest the outer 5% median method
					
				#day
				csv_row.append(FeatureData.dayValues.median_max_value_day[date][i])
				csv_row.append(FeatureData.dayValues.median_min_value_day[date][i])
				csv_row.append(FeatureData.dayValues.avg_max_value_day[date][i])
				csv_row.append(FeatureData.dayValues.avg_min_value_day[date][i])
					
				#median sunup sundown
				csv_row.append(FeatureData.dayValues.median_max_value_sunup[date][i])
				csv_row.append(FeatureData.dayValues.median_min_value_sunup[date][i])
				csv_row.append(FeatureData.dayValues.median_max_value_sundown[date][i])
				csv_row.append(FeatureData.dayValues.median_min_value_sundown[date][i])
			
				#average sunup sundown
				csv_row.append(FeatureData.dayValues.avg_max_value_sunup[date][i])
				csv_row.append(FeatureData.dayValues.avg_min_value_sunup[date][i])
				csv_row.append(FeatureData.dayValues.avg_max_value_sundown[date][i])
				csv_row.append(FeatureData.dayValues.avg_min_value_sundown[date][i])
					
#=======================DISTANCES AUF MEDIANS/AVGS=========================================================					

				#median distances of day to sunup / sundown values (minus)
				csv_row.append(FeatureData.dayValues.median_sunup_minus_sundown[date][i])
				csv_row.append(FeatureData.dayValues.median_minus_sundown[date][i])
				csv_row.append(FeatureData.dayValues.median_minus_sunup[date][i])
					
				#median relation of day to sunup / sundown values (divides)
				csv_row.append(FeatureData.dayValues.median_sunup_to_sundown[date][i])
				csv_row.append(FeatureData.dayValues.median_to_sundown[date][i])
				csv_row.append(FeatureData.dayValues.median_to_sunup[date][i])

				#average distances of day to sunup / sundown values (minus)
				csv_row.append(FeatureData.dayValues.average_sunup_minus_sundown[date][i])
				csv_row.append(FeatureData.dayValues.average_minus_sundown[date][i])
				csv_row.append(FeatureData.dayValues.average_minus_sunup[date][i])
					
				#average relation of day to sunup / sundown values (divides)
				csv_row.append(FeatureData.dayValues.average_sunup_to_sundown[date][i])
				csv_row.append(FeatureData.dayValues.average_to_sundown[date][i])
				csv_row.append(FeatureData.dayValues.average_to_sunup[date][i])
					
#=======================DISTANCES AUF MEDIANS/AVGS=========================================================					
				#distance (minus) of min and max median
				csv_row.append(FeatureData.dayValues.median_max_minus_min_day[date][i])
				csv_row.append(FeatureData.dayValues.median_max_minus_min_sunup[date][i])
				csv_row.append(FeatureData.dayValues.median_max_minus_min_sundown[date][i])
					
				#relation (devide) of min and max median
				csv_row.append(FeatureData.dayValues.median_max_to_min_day[date][i])
				csv_row.append(FeatureData.dayValues.median_max_to_min_sunup[date][i])
				csv_row.append(FeatureData.dayValues.median_max_to_min_sundown[date][i])
					
				#distance (minus) of min and max average
				csv_row.append(FeatureData.dayValues.avg_max_minus_min_day[date][i])
				csv_row.append(FeatureData.dayValues.avg_max_minus_min_sunup[date][i])
				csv_row.append(FeatureData.dayValues.avg_max_minus_min_sundown[date][i])

				#relation (devide) of min and max average
				csv_row.append(FeatureData.dayValues.avg_max_to_min_day[date][i])
				csv_row.append(FeatureData.dayValues.avg_max_to_min_sunup[date][i])
				csv_row.append(FeatureData.dayValues.avg_max_to_min_sundown[date][i])
					
#=======================VARIANCE====================================================
				csv_row.append(FeatureData.dayValues.variance_day[date][i])
				csv_row.append(FeatureData.dayValues.variance_sunup[date][i])
				csv_row.append(FeatureData.dayValues.variance_sundown[date][i])
					
				csv_row_string = ';'.join(map(str, csv_row)) 
				csv_row_string = csv_row_string + "\n"
				csv_cache[i].append(csv_row_string)

		for i in range(len(csv_cache)):
			filename = "results/"+str(i)+"_"+str(timestamp)+"_datapoint_"+str(i)+".csv"
			
			with open(filename ,'a') as fd:
				
				fd.write( "".join(csv_cache[i]))
				fd.close()



	def exportToCSV(datapoints):
		timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

		for point in datapoints:
			for i in range(len(point.rowdata)):
				filename = "results/"+str(i)+"_"+str(timestamp)+"_datapoint_"+str(i)+".csv"
				with open(filename ,'a') as fd:
						
					#writer = csv.writer(fd)
					csv_row = []
					
					csv_row.append(point.date)
					csv_row.append(point.time)
					csv_row.append(point.rowdata[i])					
					csv_row.append(point.season)
					csv_row.append(point.week_of_year)
					csv_row.append(point.quarter_of_year)
	
					csv_row.append(point.day_of_week)
					csv_row.append(point.month)
				
					csv_row.append(point.day)
					csv_row.append(point.hour)
					csv_row.append(point.daylight_saving_time)
					csv_row.append(point.sunIsShining)
					csv_row.append(point.heating_period)



					
					#point.day_median
					#point.sunup_median
					#point.sundown_median
					#point.median_sunup_minus_sundown
					#point.median_sunup_to_sundown
					#point.day_median_to_sunup
					#point.day_median_to_down
					#point.day_median_minus_down
					#point.day_median_minus_sunup
					#point.day_avg
					#point.sunup_avg
					#point.sundown_avg
					#point.avg_sunup_minus_sundown
					#point.avg_minus_sunup
					#point.avg_minus_sundown
					
					date = point.date
					
					#medians
					csv_row.append(FeatureData.dayValues.median_for_a_day[date][i])
					csv_row.append(FeatureData.dayValues.median_for_a_day_sunup[date][i])
					csv_row.append(FeatureData.dayValues.median_for_a_day_sundown[date][i])
			
					#averages
					csv_row.append(FeatureData.dayValues.average_for_a_day[date][i])
					csv_row.append(FeatureData.dayValues.average_for_a_day_sunup[date][i])
					csv_row.append(FeatureData.dayValues.average_for_a_day_sundown[date][i])

#=======================MEDIAN TO AVERAGE RELATIONS =========================================================								
					

					csv_row.append(FeatureData.dayValues.median_minus_average_day[date][i])
					csv_row.append(FeatureData.dayValues.median_minus_average_sunup[date][i])
					csv_row.append(FeatureData.dayValues.median_minus_average_sundown[date][i])

					csv_row.append(FeatureData.dayValues.median_to_average_day[date][i])
					csv_row.append(FeatureData.dayValues.median_to_average_sunup[date][i])
					csv_row.append(FeatureData.dayValues.median_to_average_sundown[date][i])
					

			
#=======================MIN/MAX VALUES AUF MEDIANS/AVGS=========================================================			
			
					#max and min values of the lowest the outer 5% median method
					
						#day
					csv_row.append(FeatureData.dayValues.median_max_value_day[date][i])
					csv_row.append(FeatureData.dayValues.median_min_value_day[date][i])
					csv_row.append(FeatureData.dayValues.avg_max_value_day[date][i])
					csv_row.append(FeatureData.dayValues.avg_min_value_day[date][i])
					
						#median sunup sundown
					csv_row.append(FeatureData.dayValues.median_max_value_sunup[date][i])
					csv_row.append(FeatureData.dayValues.median_min_value_sunup[date][i])
					csv_row.append(FeatureData.dayValues.median_max_value_sundown[date][i])
					csv_row.append(FeatureData.dayValues.median_min_value_sundown[date][i])
			
						#average sunup sundown
					csv_row.append(FeatureData.dayValues.avg_max_value_sunup[date][i])
					csv_row.append(FeatureData.dayValues.avg_min_value_sunup[date][i])
					csv_row.append(FeatureData.dayValues.avg_max_value_sundown[date][i])
					csv_row.append(FeatureData.dayValues.avg_min_value_sundown[date][i])
					
#=======================DISTANCES AUF MEDIANS/AVGS=========================================================					
					#median distances of day to sunup / sundown values (minus)
					csv_row.append(FeatureData.dayValues.median_sunup_minus_sundown[date][i])
					csv_row.append(FeatureData.dayValues.median_minus_sundown[date][i])
					csv_row.append(FeatureData.dayValues.median_minus_sunup[date][i])
					
					#median relation of day to sunup / sundown values (divides)
					csv_row.append(FeatureData.dayValues.median_sunup_to_sundown[date][i])
					csv_row.append(FeatureData.dayValues.median_to_sundown[date][i])
					csv_row.append(FeatureData.dayValues.median_to_sunup[date][i])

					#average distances of day to sunup / sundown values (minus)
					csv_row.append(FeatureData.dayValues.average_sunup_minus_sundown[date][i])
					csv_row.append(FeatureData.dayValues.average_minus_sundown[date][i])
					csv_row.append(FeatureData.dayValues.average_minus_sunup[date][i])
					
					#average relation of day to sunup / sundown values (divides)
					csv_row.append(FeatureData.dayValues.average_sunup_to_sundown[date][i])
					csv_row.append(FeatureData.dayValues.average_to_sundown[date][i])
					csv_row.append(FeatureData.dayValues.average_to_sunup[date][i])
					
#=======================DISTANCES AUF MEDIANS/AVGS=========================================================					
					#distance (minus) of min and max median
					csv_row.append(FeatureData.dayValues.median_max_minus_min_day[date][i])
					csv_row.append(FeatureData.dayValues.median_max_minus_min_sunup[date][i])
					csv_row.append(FeatureData.dayValues.median_max_minus_min_sundown[date][i])
					
					#relation (devide) of min and max median
					csv_row.append(FeatureData.dayValues.median_max_to_min_day[date][i])
					csv_row.append(FeatureData.dayValues.median_max_to_min_sunup[date][i])
					csv_row.append(FeatureData.dayValues.median_max_to_min_sundown[date][i])
					
					#distance (minus) of min and max average
					csv_row.append(FeatureData.dayValues.avg_max_minus_min_day[date][i])
					csv_row.append(FeatureData.dayValues.avg_max_minus_min_sunup[date][i])
					csv_row.append(FeatureData.dayValues.avg_max_minus_min_sundown[date][i])

					#relation (devide) of min and max average
					csv_row.append(FeatureData.dayValues.avg_max_to_min_day[date][i])
					csv_row.append(FeatureData.dayValues.avg_max_to_min_sunup[date][i])
					csv_row.append(FeatureData.dayValues.avg_max_to_min_sundown[date][i])
					
#=======================VARIANCE====================================================
					csv_row.append(FeatureData.dayValues.variance_day[date][i])
					csv_row.append(FeatureData.dayValues.variance_sunup[date][i])
					csv_row.append(FeatureData.dayValues.variance_sundown[date][i])
					
					csv_row_string = ';'.join(map(str, csv_row)) 
					csv_row_string = csv_row_string + "\n"
					fd.write(csv_row_string)

					#writer.writerows(map(lambda x: [x], csv_row))
					#out.writerows(map(lambda x: [x], fin_ids))
					#map(lambda x: [x], fin_ids)
					#writer.writerows(csv_row)
					
					#fd.write(csv_row)
					fd.close()
			
		
	def cachedIsTheSunShining(mydate, mytime):
		giventime = datetime.datetime.strptime(mytime, '%H:%M').time()

		if giventime > SunAndCalendarData.sunrises[mydate] and giventime < SunAndCalendarData.sunsets[mydate]:
			return True
		else:
			return False		