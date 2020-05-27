#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:16:19 2020

@author: rohezal
"""

import math

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

		#median to average spread and ration
		self.median_minus_average_day={}
		self.median_minus_average_sunup={}
		self.median_minus_average_sundown={}
		
		self.median_to_average_day={}
		self.median_to_average_sunup={}
		self.median_to_average_sundown={}

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
		
		#variance
		self.variance_day = {}
		self.variance_sunup = {}
		self.variance_sundown = {}
		
		
		
	def calculateFeaturesFromMedianAndAverage(self):
		for key in self.median_for_a_day.keys():
			
			#median to average metris
			self.median_minus_average_day[key] = ValueContainer.list_minus_list(self.median_for_a_day[key],self.average_for_a_day[key])
			self.median_minus_average_sunup[key] = ValueContainer.list_minus_list(self.median_for_a_day_sunup[key],self.average_for_a_day_sunup[key])
			self.median_minus_average_sundown[key] = ValueContainer.list_minus_list(self.median_for_a_day_sundown[key],self.average_for_a_day_sundown[key])
		
			self.median_to_average_day[key] = ValueContainer.list_divided_by_list(self.median_for_a_day[key],self.average_for_a_day[key])
			self.median_to_average_sunup[key] = ValueContainer.list_divided_by_list(self.median_for_a_day_sunup[key],self.average_for_a_day_sunup[key]) 
			self.median_to_average_sundown[key] = ValueContainer.list_divided_by_list(self.median_for_a_day_sundown[key],self.average_for_a_day_sundown[key])
			
			#sunup vs sundown
			
			self.median_sunup_minus_sundown[key] = ValueContainer.list_minus_list(self.median_for_a_day_sunup[key],self.median_for_a_day_sundown[key])
			self.median_minus_sunup[key] = ValueContainer.list_minus_list(self.median_for_a_day[key],self.median_for_a_day_sunup[key])
			self.median_minus_sundown[key] = ValueContainer.list_minus_list(self.median_for_a_day[key],self.median_for_a_day_sundown[key])
				
			self.median_sunup_to_sundown[key] = ValueContainer.list_divided_by_list(self.median_for_a_day_sunup[key],self.median_for_a_day_sundown[key])
			self.median_to_sunup[key] = ValueContainer.list_divided_by_list(self.median_for_a_day[key],self.median_for_a_day_sunup[key])
			self.median_to_sundown[key] = ValueContainer.list_divided_by_list(self.median_for_a_day[key],self.median_for_a_day_sundown[key])
				
			self.average_sunup_minus_sundown[key] = ValueContainer.list_minus_list(self.average_for_a_day_sunup[key],self.average_for_a_day_sundown[key])
			self.average_minus_sunup[key] = ValueContainer.list_minus_list(self.average_for_a_day[key],self.average_for_a_day_sunup[key])
			self.average_minus_sundown[key] = ValueContainer.list_minus_list(self.average_for_a_day[key],self.average_for_a_day_sundown[key])
				
			self.average_sunup_to_sundown[key] = ValueContainer.list_divided_by_list(self.average_for_a_day_sunup[key],self.average_for_a_day_sundown[key])
			self.average_to_sunup[key] = ValueContainer.list_divided_by_list(self.average_for_a_day[key],self.average_for_a_day_sunup[key])
			self.average_to_sundown[key] = ValueContainer.list_divided_by_list(self.average_for_a_day[key],self.average_for_a_day_sundown[key])
	
			#extreme values				
			self.median_max_minus_min_day[key] = ValueContainer.list_minus_list(self.median_max_value_day[key],self.median_min_value_day[key])
			self.median_max_minus_min_sunup[key] = ValueContainer.list_minus_list(self.median_max_value_sunup[key],self.median_min_value_sunup[key])
			self.median_max_minus_min_sundown[key] = ValueContainer.list_minus_list(self.median_max_value_sundown[key],self.median_min_value_sundown[key])

			self.avg_max_minus_min_day[key] = ValueContainer.list_minus_list(self.avg_max_value_day[key],self.avg_min_value_day[key])
			self.avg_max_minus_min_sunup[key] = ValueContainer.list_minus_list(self.avg_max_value_sunup[key],self.avg_min_value_sunup[key])
			self.avg_max_minus_min_sundown[key] = ValueContainer.list_minus_list(self.avg_max_value_sundown[key],self.avg_min_value_sundown[key])
				
			self.median_max_to_min_day[key] = ValueContainer.list_divided_by_list(self.median_max_value_day[key],self.median_min_value_day[key])
			self.median_max_to_min_sunup[key] = ValueContainer.list_divided_by_list(self.median_max_value_sunup[key],self.median_min_value_sunup[key])
			self.median_max_to_min_sundown[key] = ValueContainer.list_divided_by_list(self.median_max_value_sundown[key],self.median_min_value_sundown[key])

			self.avg_max_to_min_day[key] = ValueContainer.list_divided_by_list(self.avg_max_value_day[key],self.avg_min_value_day[key])
			self.avg_max_to_min_sunup[key] = ValueContainer.list_divided_by_list(self.avg_max_value_sunup[key],self.avg_min_value_sunup[key])
			self.avg_max_to_min_sundown[key] = ValueContainer.list_divided_by_list(self.avg_max_value_sundown[key],self.avg_min_value_sundown[key])
				
	def list_minus_list(list1, list2):
		newlist = []
		for i in range(len(list1)):
			newlist.append(list1[i]-list2[i])
		return newlist				
		
	def list_divided_by_list(list1,list2):
		newlist = []
		for i in range(len(list1)):
			if(list2[i] == 0):
				newlist.append(0)
			else:
				newlist.append(list1[i]/list2[i])
		return newlist