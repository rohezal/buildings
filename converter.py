#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 00:06:57 2020

@author: rohezal
"""

import csv
import sys

number_of_arguments = len(sys.argv)
if(number_of_arguments == 2):
	filename = sys.argv[1]
	
else:
	print("usage: converter.py name_of_the_file.csv. Using now converted_BRICS.csv as a default file")
	filename = 'converted_BRICS.csv'	

outfile = open('converted_'+filename, 'w')
csvwriter = csv.writer(outfile )

with open(filename) as csv_file_brics:    
    
    csv_reader_brics = csv.reader(csv_file_brics, delimiter=',')
    for row in csv_reader_brics:
        newrow = []
        for element in row:
            if(":" not in element):
                element = float(element.replace(',', '.'))
            else:
                element = "\"" + element + "\""
            newrow.append(element)                
                
        #print(row)
        #print(newrow)                
        #print("=============")                
        #print(row)    
        csvwriter.writerow(newrow)                                
outfile.close