from xml.dom import minidom
import xml.etree.ElementTree as ET
import os

#Place files to be counted in same directory as this python file.

xml_files = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".xml"):
            xml_files.append(file)
    break

print(xml_files)

dust_objects = 0
bead_objects = 0

for file in xml_files:
    tree = ET.parse(file)
    root=tree.getroot()
    for elem in root:
        if elem.tag=='object':
            for elem2 in elem:
                if elem2.tag=='name' and elem2.text == 'dust':
                    dust_objects += 1
                if elem2.tag=='name' and elem2.text == 'bead':
                    bead_objects += 1

           
print("total objects: " + str(dust_objects + bead_objects))
print("bead objects: " + str(bead_objects))
print("dust_objects: " + str(dust_objects))
