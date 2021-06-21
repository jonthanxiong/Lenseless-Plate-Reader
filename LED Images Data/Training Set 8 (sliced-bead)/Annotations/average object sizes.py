import xml.etree.ElementTree as ET
import os

#Place files to be considered in same directory as this python file.

xml_files = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".xml"):
            xml_files.append(file)
    break

total_area=0
total_height=0
total_width=0
total_objects=0

for file in xml_files:
    tree=ET.parse(file)
    root=tree.getroot()

    for elem in root.iter('object'):
        for elem2 in elem:
            if elem2.tag=='bndbox':
                width = int(elem2[2].text)-int(elem2[0].text)
                height = int(elem2[3].text)-int(elem2[1].text)
                total_area+=width*height
                total_height+=height
                total_width+=width
        total_objects+=1


print("Average Area: " + str(total_area/total_objects))
print("Average Width: " + str(total_width/total_objects))
print("Average Height: " + str(total_height/total_objects))
    
