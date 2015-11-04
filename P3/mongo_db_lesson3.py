# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 09:48:40 2015
@author: ger
Data Wrangling with MongoDB lesson 3
"""

"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint

INPUT_FILE = 'data/autos.csv'
OUTPUT_GOOD = 'data/autos-valid.csv'
OUTPUT_BAD = 'data/FIXME-autos.csv'

GOOD_DATA = []
BAD_DATA = []

def process_file(input_file, output_good, output_bad):

    with open(input_file, "rb") as f:
        reader = csv.DictReader(f, delimiter=',')
        headers = reader.fieldnames
        #COMPLETE THIS FUNCTION
        psyindex = headers.index('productionStartYear')
        counter = 0
        for row in reader:
            # replace check by if URI is not from dbpedia.org           
            if counter >= 3:
                date = row["productionStartYear"]
                parts = date.split('-')
                year = parts[0]
                if year_valid(year):
                    row["productionStartYear"] = year
                    GOOD_DATA.append(row)
                else:
                    BAD_DATA.append(row)
            counter += 1

    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    write_to_file(OUTPUT_GOOD, headers, GOOD_DATA)
    write_to_file(OUTPUT_BAD, headers, BAD_DATA)
    
def year_valid(year):
    print year
    if year == 'NULL':
        return False
    else:
        year_int = int(year)
        if year_int < 1886 or year_int > 2014:
            return False
    return True

def write_to_file(filename, headers, data):
     with open(filename, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def testAutos():
    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)

testAutos()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then
clean it up. In the first exercise we want you to audit the datatypes that can be found in some 
particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a SET of the types
that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint

CITIES = 'data/cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]
def audit_file(filename, fields):
    fieldtypes = {}

    with open(filename, "rb") as f:
        reader = csv.DictReader(f, delimiter=',')
        headers = reader.fieldnames
        next(reader)
        next(reader)
        next(reader)
        for field in FIELDS:
            fieldtypes[field] = set()
        for row in reader:
            for field in FIELDS:
                value = row[field]
                value_type = get_type(value)
                fieldtypes[field].add(value_type)
    return fieldtypes

def get_type(value):
    if value == "NULL":
        return type(None)
    elif value.startswith("{"):
        return type([])
    else:
        try:
            value_float = float(value)
            return type(1.1)
        except:
            print "error"


def testQuality():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
testQuality()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'data/cities.csv'

def fix_area(area):
    if area == "NULL":
        return None
    elif area.startswith("{") and area.endswith("}"):
        area = area[1:len(area)-1]
        area_parts = area.split("|")
        if (len(area_parts[0]) > len(area_parts[1])) :
            return float(area_parts[0])
        else:
            return float(area_parts[1])
    else:
        return float(area)



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def testFixArea():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[8]["areaLand"] == 55166700.0
    assert data[3]["areaLand"] == None


testFixArea()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

In the previous quiz you recognized that the "name" value can be an array (or list in Python terms).
It would make it easier to process and query the data later, if all values for the name 
would be in a Python list, instead of being just a string separated with special characters, like now.

Finish the function fix_name(). It will recieve a string as an input, and it has to return a list
of all the names. If there is only one name, the list with have only one item in it, if the name is "NULL",
the list should be empty.
The rest of the code is just an example on how this function can be used
"""
import codecs
import csv
import pprint

CITIES = 'data/cities.csv'

def fix_name(name):
    result = []
    if name == "NULL":
        return result
    elif name.startswith("{") and name.endswith("}"):
        name = name[1:len(name)-1]
        name_parts = name.split("|")
        result.append(name_parts[0])
        result.append(name_parts[1])
        return result
    else:
        result.append(name)
        return result


def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        #skipping the extra metadata
        for i in range(3):
            l = reader.next()
        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "name" in line:
                line["name"] = fix_name(line["name"])
            data.append(line)
    return data


def testFixName():
    data = process_file(CITIES)

    print "Printing 20 results:"
    for n in range(20):
        pprint.pprint(data[n]["name"])

    assert data[14]["name"] == ['Negtemiut', 'Nightmute']
    assert data[9]["name"] == ['Pell City Alabama']
    assert data[3]["name"] == ['Kumhari']

testFixName()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

If you look at the full city data, you will notice that there are couple of values that seem to provide
the same information in different formats: "point" seems to be the combination of "wgs84_pos#lat" and "wgs84_pos#long".
However we do not know if that is the case and should check if they are equivalent.

Finish the function check_loc(). It will recieve 3 strings, first will be the combined value of "point" and then the
"wgs84_pos#" values separately. You have to extract the lat and long values from the "point" and compare
to the "wgs84_pos# values and return True or False.

Note that you do not have to fix the values, just determine if they are consistent. To fix them in this case
you would need more information. Feel free to discuss possible strategies for fixing this on the discussion forum.

The rest of the code is just an example on how this function can be used.
Changes to "process_file" function will not be take into account.
"""
import csv
import pprint

CITIES = 'data/cities.csv'

def check_loc(point, lat, longi):
    parts = point.split(" ")
    if parts[0] == lat and parts[1] == longi :
        return True
    else:
        return False


def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        #skipping the extra matadata
        for i in range(3):
            l = reader.next()
        # processing file
        for line in reader:
            # calling your function to check the location
            result = check_loc(line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"])
            if not result:
                print "{}: {} != {} {}".format(line["name"], line["point"], line["wgs84_pos#lat"], line["wgs84_pos#long"])
            data.append(line)

    return data

def testFixLocation():
    assert check_loc("33.08 75.28", "33.08", "75.28") == True
    assert check_loc("44.57833333333333 -91.21833333333333", "44.5783", "-91.2183") == False

testFixLocation()
