# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
import xlrd
import os
import csv
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    #data = [['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']]
    data = {}
    
    regions = sheet.row_values(0, start_colx=0, end_colx=None)
    regions = regions[1:-1]
    for i in range(len(regions)):
        row = {
            'Max Load': None,
            'Year': None,
            'Month': None,
            'Day': None,
            'Hour': None
        }
        values = sheet.col_values(i+1, start_rowx=1, end_rowx=None)
        row['Max Load'] = max(values)
        max_value_index = values.index(row['Max Load']) + 1
        max_time = sheet.cell_value(max_value_index, 0)
        time = xlrd.xldate_as_tuple(max_time, 0) # (year, month, day, hour, 0, 0)
        row['Year'] = time[0]
        row['Month'] = time[1]
        row['Day'] = time[2]
        row['Hour'] = time[3]
        data[regions[i]] = row
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    return data

     
def save_file(data, filename):
    with open(filename, "w") as f:
        w = csv.writer(f, delimiter='|')
        w.writerow(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
        for s in data:
            w.writerow([s, data[s]['Year'], data[s]['Month'], data[s]['Day'], data[s]['Hour'], data[s]['Max Load']])

    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}
    
    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, ['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load'], delimiter="|")
        #print csvfile.next()
        #print csvfile.next()
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]

        
test()