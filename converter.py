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
	filename = 'BRICS_orignal_.csv'	

outfile = open('converted_'+filename, 'w', newline="")
csvwriter = csv.writer(outfile )

with open(filename, newline="", encoding='ISO-8859-1') as csv_file_brics:	
	
	csv_reader_brics = csv.reader(csv_file_brics, delimiter=';')
	for row in csv_reader_brics:
		newrow = []
		
		if(len(row) > 0):
			if((row[0][0]).isnumeric()):
				for element in row:
					if (element == "" or element == "MV"):
						element="NaN"		

					elif(":" not in element):
						try:
							element = float(element.replace(',', '.'))
						except Exception as e:
							print("Element: " + element)							
							print(e)
							sys.exit(1)
					else:
						element = "\"" + element + "\""
					newrow.append(element)				
		if(len(newrow) > 0):
			csvwriter.writerow(newrow)								
outfile.close
