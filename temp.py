# -*- coding: utf-8 -*-

import csv
import statistics
import ephem
import datetime
from ephem import cities
import featurecalculation



sunrises = {} #dictonary to lookup when the sun rises
sunsets = {} #dictonary to lookup when the sun sets

datalist = [] #list of csv with calculated future

INITVALUE = -666999
timezone_delta = 1 #relative to UTC which is GMT (1 hour before Berlin)

class ValueContainer:
    def __init__(self):
        self.median_for_a_day = {}
        self.median_for_a_day_sunup= {}
        self.median_for_a_day_sundown= {}
        self.average_for_a_day = {}
        self.average_for_a_day_sunup= {}
        self.average_for_a_day_sundown= {}
        
dayValues = ValueContainer()        
        
class FeatureData:
    def __init__(self, data):
        #datestring = data[0].replace("\"", "") #take the first row and assume it is date and time. e.g. 1.1.2020 19:30 
        datestring = data[0] #take the first row and assume it is date and time. e.g. 1.1.2020 19:30 
        self.date = datestring.split()[0] #split the date part. 1.1.2020 19:30 -> 1.1.2020
        self.time = datestring.split()[1] #split the time part. 1.1.2020 19:30 -> 19:30
        self.rowdata = data[1:] #take each row after the first one, since the first one is date and time
        self.sunIsShining=False
        self.heating_period=False
        self.outside_temperature=INITVALUE
        
        self.day_median=[]
        self.sunup_median=[]
        self.sundown_median=[]
        self.sunup_minus_sundown=[]
        self.sunup_to_sundown=[]
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

        self.month=""
        self.my_own_feature=INITVALUE
        
    def calculateIfSunIsShining(self):
        self.sunIsShining=cachedIsTheSunShining(self.date, self.time)
        #self.sunIsShining=isTheSunShining(self.date, self.time)
        
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
                
                
                
        #print (day_features)
        
        
        dayValues.median_for_a_day[date] = featurecalculation.median_for_lists(day_features)
        dayValues.median_for_a_day_sunup[date] = featurecalculation.median_for_lists(sunup_features)
        dayValues.median_for_a_day_sundown[date] = featurecalculation.median_for_lists(sundown_features)
        
        dayValues.average_for_a_day[date] = featurecalculation.average_for_lists(day_features)
        dayValues.average_for_a_day_sunup[date] = featurecalculation.average_for_lists(sunup_features)
        dayValues.average_for_a_day_sundown[date] = featurecalculation.average_for_lists(sundown_features)
    
        #print(day_buffer_list);
        
    def dateToMonth(date):
        date = date
    def dateToHeating(date):
        date=date
        
    def copyFeaturesFromDictonaryToFeatureData(datapoints):
        for point in datapoints:
            point.day_median = dayValues.median_for_a_day[point.date]
        
        
    def exportToCSV(datapoints):
        print("implement me")
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

def cachedIsTheSunShining(mydate, mytime):
    giventime = datetime.datetime.strptime(mytime, '%H:%M').time()

    if giventime > sunrises[mydate] and giventime < sunsets[mydate]:
        return True
    else:
        return False
    
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
    
    sunrises[mydate] = sunrise
    sunsets[mydate] = sunset
    
   
    if giventime > sunrise and giventime < sunset:
        return True
    else:
        return False
    
    


featurecalculation.unit_test()

    
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
    
    
    
    
    