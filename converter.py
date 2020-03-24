#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 00:06:57 2020

@author: rohezal
"""

import csv

outfile = open('converted_BRICS.csv', 'w')
csvwriter = csv.writer(outfile )

with open('BRICS.csv') as csv_file_brics:    
    
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