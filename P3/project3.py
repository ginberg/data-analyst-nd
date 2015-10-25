import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
        tags = {}
        tree = ET.parse(filename)
        for elem in tree.iter():
            if elem.tag in tags:
                tags[elem.tag] = tags[elem.tag] + 1                
            else:
                tags[elem.tag] = 1
        return tags


def test():

    tags = count_tags('data/utrecht_map.osm')
    pprint.pprint(tags)
    
test