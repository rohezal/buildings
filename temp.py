# -*- coding: utf-8 -*-

import csv
import statistics
import ephem
import datetime
from ephem import cities

sunrises = {} #dictonary to lookup when the sun rises
sunsets = {} #dictonary to lookup when the sun sets

datalist = [] #list of csv with calculated future

INITVALUE = -666999
timezone_delta = 1 #relative to UTC which is GMT (1 hour before Berlin)

class FeatureData:
    def __init__(self, data):
        datestring = data[0] #take the first row and assume it is date and time. e.g. 1.1.2020 19:30 
        self.date = datestring.split()[0] #split the date part. 1.1.2020 19:30 -> 1.1.2020
        self.time = datestring.split()[1] #split the time part. 1.1.2020 19:30 -> 19:30
        self.rowdata = data[1:] #take each row after the first one, since the first one is date and time
        self.sunIsShining=False
        self.day_median=INITVALUE
        self.sunup_median=INITVALUE
        self.sundown_median=INITVALUE
        self.sunup_minus_sundown=INITVALUE
        self.sunup_to_sundown=INITVALUE
        self.day_median_to_sunup=INITVALUE
        self.day_median_to_down=INITVALUE
        self.day_median_minus_down=INITVALUE
        self.day_median_minus_sunup=INITVALUE
        self.day_avg = INITVALUE
        self.sunup_avg= INITVALUE
        self.sundown_avg= INITVALUE
        self.month=""
        self.heating_period=False
        self.outside_temperature=INITVALUE
        
    def calculateIfSunIsShining(self):
        self.sunIsShining=cachedIsTheSunShining(self.date, self.time)
        #self.sunIsShining=isTheSunShining(self.date, self.time)
        
#def loadCSVAndComputeSunrise(filename):
    
        
#def calculateFeatures(datapoints):
    
            
        

def average(input):
    sum = 0.0
    for element in input:
        sum = sum + element
    sum = sum / len(input)        
    return sum

def cachedIsTheSunShining(mydate, mytime):
    giventime = datetime.datetime.strptime(mytime, '%H:%M').time()

    if giventime > sunrises[mydate] and giventime < sunsets[mydate]:
        return True
    else:
        return False
    
def fillCache(csv_reader):
    lastdate = "" 
    for row in csv_reader:
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
    
    sunrises[mydate] = sunrise
    sunsets[mydate] = sunset
    
   
    if giventime > sunrise and giventime < sunset:
        return True
    else:
        return False
    
    


    
with open('BRICS.csv') as csv_file_brics:    
    csv_reader_brics = csv.reader(csv_file_brics, delimiter=',')
    fillCache(csv_reader_brics)

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
    print(isTheSunShining("2020/3/12", "4:30"))
    print(isTheSunShining("2020/3/12", "7:30"))
    print(isTheSunShining("2020/3/12", "20:30"))
    print(isTheSunShining("2012/1/1", "7:30"))
    print(isTheSunShining("2012/1/1", "6:20"))
    
    print("======================================================")

    print(cachedIsTheSunShining("2020/3/12", "4:30"))
    print(cachedIsTheSunShining("2020/3/12", "7:30"))
    print(cachedIsTheSunShining("2020/3/12", "20:30"))

    print(str(sunrises["2020/3/12"]) + " " + str(sunsets["2020/3/12"]))
    
    print("======================================================")
    sunrises['big'] = datetime.datetime.strptime("8:00", '%H:%M').time()
    sunrises['small'] = datetime.datetime.strptime("7:00", '%H:%M').time()
    print("Test")
    print(sunrises["2012/1/1"] < sunrises['big'] )
    print(sunrises["2012/1/1"] < sunrises['small'] )
    
    
    
    
    