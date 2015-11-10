#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from lxml import etree
import pprint
import re
import codecs
import json
from collections import defaultdict
import matplotlib.pyplot as plt

FILENAME='data/utrecht_netherlands.osm'
FILENAME_OUT='data/utrecht.json'
SAMPLE_FILE = "data/utrecht-sample.osm"

EXPECTED_STREET_NAMES = ["straat", "laan", "plein", "dreef", "singel", "weg", "baan", "steeg", "dijk", "veld", "hof", "werf", "poort", "markt","gracht","weide",
                         "plantsoen", "pad", "kade", "polder", "veer", "dam", "park", "berg", "spoor", "hoeve", "kamp", "kwartier", "weerd", "vaart","vlinder"]
                         
STREET_NAME_ABBREVIATIONS = ["W.Z", "O.Z."]
DUTCH_POSTAL_CODE_REGEX = "^[0-9]{4}\s*[a-zA-Z]{2}$"

"""Audit data the osm file."""
def auditMapData(filename):
    tags = {}
    street_types = []
    wrong_postal_codes = []
    unexpected_postal_codes = []
    context = ET.iterparse(filename, events=('start','end'))
    context = iter(context)
    event, root = context.next()
    for event, element in context:
        if event=='end':    
            if element.tag in tags:
                tags[element.tag] = tags[element.tag] + 1                
            else:
                tags[element.tag] = 1
            
            if element.tag == "node" or element.tag == "way":
                for tag in element.iter("tag"):
                    if is_street_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])
                    #elif is_postal_code(tag):
                     #   audit_postal_code_format(wrong_postal_codes, tag.attrib['v'])        
                      #  audit_postal_code_region(unexpected_postal_codes, tag.attrib['v']) 
                    elif is_cuisine(tag):
                        if tag.attrib['v'] == "":
                            print "empty cuisine!"
        root.clear()
    del context
    
    print "Number of main tags:"
    pprint.pprint(tags)              
    print "Unexpected street types:", set(street_types)
    print "Wrong postal codes:", set(wrong_postal_codes)
    print "Unexpected postal codes:", set(unexpected_postal_codes)
    return tags 
 
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
    
def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")
    
def is_cuisine(elem):
    return (elem.attrib['k'] == "cuisine")

def audit_street_type(street_types, street_name):
    if not street_name.endswith(tuple(EXPECTED_STREET_NAMES)):
        street_types.append(street_name)

def audit_postal_code_format(postal_codes, postal_code):
    pattern = re.compile(DUTCH_POSTAL_CODE_REGEX)
    if not pattern.match(postal_code):
        postal_codes.append(postal_code)
        
def audit_postal_code_region(postal_codes, postal_code):
    if not postal_code.startswith("35"):
        postal_codes.append(postal_code)
        
"""Clean data the osm file."""
def cleanMapData(filename):
    context = ET.iterparse(filename, events=('start','end'))
    context = iter(context)
    event, root = context.next()
    for event, element in context:
        if event=='end':    
            if element.tag == "node":
                for tag in element.iter("tag"):
                    if is_street_name(tag):
                        clean_street_name(tag)
        root.clear()
    del context
    print "Unexpected street types:", set(cleaned_streets)

def clean_street_name(tag):
    street_name = tag.attrib['v']    
    if "W.Z." in  street_name:
        tag.attrib['v']  = street_name.replace("W.Z.", "Westzijde") 
    elif "O.Z." in  street_name:
        tag.attrib['v']  = street_name.replace("O.Z.", "Oostzijde") 
        
"""
Convert the xml data to a JSON object of the form
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def format_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        #print element
        node["id"] = getAttribute(element, "id")
        node["visible"] = getAttribute(element, "visible")
        node["type"] = element.tag
        position = []
        latitude = getAttribute(element, "lat")
        if latitude is not None:
            position.append(float(latitude))
        longitude = getAttribute(element, "lon")    
        if longitude is not None:
            position.append(float(longitude))
        node["pos"] = position
        created = {}
        created["changeset"] = getAttribute(element, "changeset")        
        created["user"] = getAttribute(element, "user")
        created["version"] = getAttribute(element, "version")
        created["uid"] = getAttribute(element, "uid")
        created["timestamp"] = getAttribute(element, "timestamp")
        node["created"] = created
        
        refs = []
        ndElements = element.findall("nd")
        if ndElements is not None:
            for nd in ndElements:
                refs.append(getAttribute(nd, "ref"))
        if len(refs) >0 :
            node["node_refs"] = refs
    
        address = {}
        tagElements = element.findall("tag")
        if tagElements is not None:
            for tagElem in tagElements:
                if getAttribute(tagElem,"k") == "addr:street":
                    address["street"] = getAttribute(tagElem, "v")
                elif getAttribute(tagElem,"k") == "addr:housenumber":
                    address["housenumber"] = getAttribute(tagElem, "v")
                elif getAttribute(tagElem,"k") == "addr:postcode":
                    address["postcode"] = getAttribute(tagElem, "v")  
                elif getAttribute(tagElem,"k") == "addr:city":
                    address["city"] = getAttribute(tagElem, "v")
                elif getAttribute(tagElem,"k") == "amenity":
                    node["amenity"] = getAttribute(tagElem, "v")
                elif getAttribute(tagElem,"k") == "cuisine":
                    node["cuisine"] = getAttribute(tagElem, "v")                     
        if bool(address):       
            node["address"] = address
        return node
    else:
        return None
    
def getAttribute(element, attribute):
     return element.get(attribute)

def convertToJson(file_in, pretty = False):
    file_out = filename_out.format(file_in)
    with codecs.open(file_out, "w") as fo:
        context = ET.iterparse(file_in,events=('start','end'))
        context = iter(context)
        event, root = context.next()
        for event, element in context:
            if event=='end':
                el = shape_element(element)
                if el:
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
            root.clear()
        del context
        
def cleanAndConvertToJson(file_in, pretty = False):
    file_out = FILENAME_OUT.format(file_in)
    with codecs.open(file_out, "w") as fo:
        context = ET.iterparse(file_in,events=('start','end'))
        context = iter(context)
        event, root = context.next()
        for event, element in context:
            if event=='end':
                #clean
                if element.tag == "node":
                    for tag in element.iter("tag"):
                        if is_street_name(tag):
                            clean_street_name(tag)
                
                #format element to it's desired format
                formatted_element = format_element(element)
                if formatted_element:
                    if pretty:
                        fo.write(json.dumps(formatted_element, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(formatted_element) + "\n")
            root.clear()
        del context


# Create sample
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag
    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# Create sample from original file
def createSample():
    with open(SAMPLE_FILE, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')

        # Write every 800th top level element
        for i, element in enumerate(get_element(filename)):
            if i % 800 == 0:
                output.write(ET.tostring(element, encoding='utf-8'))                
        output.write('</osm>')

def plotTopCuisine():
    cuisinesMap = {}
    cuisinesLabels =[]
    from pymongo import MongoClient
    import numpy as np
    client = MongoClient('localhost:27017')
    db = client.test
    top_cuisine = db.utrecht.aggregate([{"$match":{"cuisine":{"$exists":1}}}, {"$group":{"_id":"$cuisine",
                           "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])
    i = 0
    for cuisine in top_cuisine:
        cuisinesMap[i] = cuisine["count"]
        cuisinesLabels.append(cuisine["_id"])
        i = i + 1

    pos = np.arange(len(cuisinesMap.keys()))
    width = 1.0     # gives histogram aspect to the bar diagram
    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(cuisinesLabels)
    plt.bar(cuisinesMap.keys(), cuisinesMap.values(), width, color='blue')
    plt.xlabel('Cuisine')
    plt.ylabel('Frequency')
    plt.title('Top 10 cuisines in Utrecht')
    plt.show()
    
auditMapData(FILENAME)
#auditMapData(FILENAME)
#cleanMapData(filenameS)
#convertToJson(filename)
#scleanAndConvertToJson(FILENAME)
#createSample()
#plotTopCuisine()