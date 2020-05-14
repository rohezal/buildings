#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:56:53 2020

@author: rohezal
"""

import BuildingFeatures
from BuildingFeatures import FeatureData

def unittest_dateToIsHeatingPeriod():
	print("unittest_dateToIsHeatingPeriod")
	date  = "09.01.2020"
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))

	date  = "09.02.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.03.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))

	date  = "09.04.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.05.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.06.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.07.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.08.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.09.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.10.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.11.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))
	
	date  = "09.12.2020"	
	result = FeatureData.dateToIsHeatingPeriod(date)
	print (date +": " + str(result))

def unittest_dateToMonth():
	print("unittest_dateToMonth")
	date  = "09.01.2020"
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))

	date  = "09.02.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))

	date  = "09.03.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))

	date  = "09.04.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.05.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.06.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.07.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.08.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.09.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.10.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.11.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
	date  = "09.12.2020"	
	result = FeatureData.dateToMonth(date)
	print (date +": " + str(result))
	
def unittest_dayOfWeek():
	print("unittest_dayOfWeek")

	date  = "04.05.2020"
	result = FeatureData.dateToDayOfWeek(date)
	print (date +": " + str(result))

	date  = "05.05.2020"
	result = FeatureData.dateToDayOfWeek(date)
	print (date +": " + str(result))

	date  = "06.05.2020"
	result = FeatureData.dateToDayOfWeek(date)
	print (date +": " + str(result))

	date  = "07.05.2020"
	result = FeatureData.dateToDayOfWeek(date)
	print (date +": " + str(result))

	date  = "08.05.2020"
	result = FeatureData.dateToDayOfWeek(date)
	print (date +": " + str(result))

	date  = "09.05.2020"
	result = FeatureData.dateToDayOfWeek(date)
	print (date +": " + str(result))

	date  = "10.05.2020"
	result = FeatureData.dateToDayOfWeek(date)
	print (date +": " + str(result))

unittest_dateToIsHeatingPeriod()
unittest_dateToMonth()
unittest_dayOfWeek()
