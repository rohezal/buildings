# -*- coding: utf-8 -*-

import csv
import statistics
import ephem
import datetime


def average(input):
    sum = 0.0
    for element in input:
        sum = sum + element
    sum = sum / len(input)        
    return sum

def isTheSunShining(mydate, mytime):
    braunschweig = ephem.Observer()
    braunschweig.date = mydate
    braunschweig.lat, braunschweig.lon = '52.155738', '10.313623'
    
    floatime = braunschweig.next_rising(ephem.Sun())
    edate = ephem.Date(floatime)
    sunrise = edate.datetime().time()
    giventime = datetime.datetime.strptime(mytime, '%H:%M').time()
 
    if giventime < sunrise:
        return False
    else:
        return True
    
    

class PreProcessingResults:
    row_temp = [] 

with open('yearly.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    counter = 0
    
    temp_germany = []
    
    for row in csv_reader:
        if counter == 0:
            print(row[-1])
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
    print(isTheSunShining("2012/1/1", "7:30"))
    print(isTheSunShining("2012/1/1", "6:20"))
    
    