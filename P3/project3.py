#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from lxml import etree
import pprint
import re
import codecs
import json
from collections import defaultdict

filename='data/utrecht_netherlands.osm'
filenameS='data/utrecht-map-small.osm'
filenameS_out='data/utrecht-map-small-cleaned.osm'
filename_out='data/utrecht-temp.json'
expected_street_types = ["straat", "laan", "plein", "dreef", "singel", "weg", "baan", "steeg", "dijk", "veld", "hof", "werf", "poort", "markt","gracht","weide",
                         "plantsoen", "pad", "kade", "polder", "veer", "dam", "park", "berg", "spoor", "hoeve", "kamp", "kwartier", "weerd", "vaart","vlinder"]
                         
abbreviations = ["W.Z", "O.Z."]

"""Audit data the osm file."""
def auditMapData(filename):
    tags = {}
    street_types = []
    postal_codes = []
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
                    elif is_postal_code(tag):
                        audit_postal_code(postal_codes, tag.attrib['v'])        
        root.clear() #clear needed because otherwise the element remains in memory!
    del context
    #for elem in tree.iter():
    print "Number of main tags:"
    pprint.pprint(tags)              
    print "Unexpected street types:", set(street_types)
    print "Unexpected postal codes:", set(postal_codes)
    return tags 
 
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
    
def is_postal_code(elem):
    return (elem.attrib['k'] == "postal_code")
    
def audit_street_type(street_types, street_name):
    if not street_name.endswith(tuple(expected_street_types)):
        street_types.append(street_name)

def audit_postal_code(postal_codes, postal_code):
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
        root.clear() #clear needed because otherwise the element remains in memory!
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
            root.clear() #clear needed because otherwise the element remains in memory!
        del context
        
def cleanAndConvertToJson(file_in, pretty = False):
    file_out = filename_out.format(file_in)
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
            root.clear() #clear needed because otherwise the element remains in memory!
        del context
    
#auditMapData(filename)
#cleanMapData(filenameS)
#convertToJson(filename)
cleanAndConvertToJson(filenameS)
#do queries with pymongo

