#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:09:01 2020

@author: rohezal
"""

import statistics


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
        print (temp)
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

def upper_average(input, offset = None):
    if(len(input) == 1):
        return list[0]
    
    if(offset == None):
        offset = int(1+len(input)/50)

    sum = 0.0

    temp = input.copy()
    temp.sort()
    temp = temp[-offset:]
    
    for element in temp:
        sum = sum + element
    sum = sum / len(temp)        
    return sum

def lower_average(input, offset = None):
    if(len(input) == 1):
        return list[0]
    
    sum = 0.0
    
    if(offset == None):
        offset = int(1+len(input)/50)
    
    temp = input.copy()
    temp.sort()
    temp = temp[:offset]
    
    for element in temp:
        sum = sum + element
    sum = sum / len(temp)        
    return sum

def lower_average_list(input, offset = None):
   returnlist = []
   for element in input:
        returnlist.append(lower_average(element,offset))
   return returnlist
    
def upper_average_list(input, offset = None):
    returnlist = []
    for element in input:
        returnlist.append(upper_average(element,offset))
    return returnlist
    



#day_buffer_list = [ [1,2,3,4,5,6], [1,2,3,4,5,6], [1,2,3,4,5,6], [1,2,3,4,5,6], [10,2*2,3*3,4*4,5*5,6*6], [-1,-2,-3,-4,-5,-6] ]
#day_buffer_sunup_list = [ [1,2,3,4,5,6], [1,2,3,4,5,6], [-1,-2,-3,-4,-5,-6] ]
#day_buffer_sundown_list = [ [1,2,3,4,5,6], [1,2,3,4,5,6], [-1,-2,-3,-4,-5,-6] ]
        
#we have the data in this format t_in, t_out, p_in,p_out per datapoint. now we need the value for all datapoints of a day
#number_of_values_per_row =len(day_buffer_list[0]) #the number of different values per row is the same
#day_features = []
#sunup_features = []
#sundown_features = []
        
#for i in range(number_of_values_per_row):
#    day_features.append([]) #add a list for each column
#    sunup_features.append([]) #add a list for each column
#    sundown_features.append([]) #add a list for each column
            
#for row in day_buffer_list:
#    for i in range(len(row)):
#        day_features[i].append(row[i])
        
#for row in day_buffer_sunup_list:
#      for i in range(len(row)):
#          sunup_features[i].append(row[i])

#for row in day_buffer_sundown_list:
#    for i in range(len(row)):
#        sundown_features[i].append(row[i])

#offset = int(len(day_features)/50)
        

#avgl = average_for_lists(day_features)        
#avgll = lower_average_list(day_features)
#avglu = upper_average_list(day_features)
#medl = median_for_lists(day_features)
#med_lowerl = lower_median_for_lists(day_features,offset)
#med_upperl = upper_median_for_lists(day_features,offset)

#avg = average(day_features[0])        
#med = statistics.median(day_features[0])
#med_lower = day_features[0][offset]
#med_upper = day_features[0][-offset]
    
#avg2median = avg/med
#max2min = med_upper/med_lower
#med2max = med / med_upper
#med2min = med / med_lower
#max_minus_min = abs(med_upper-med_lower)
        