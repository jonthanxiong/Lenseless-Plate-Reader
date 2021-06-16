from xml.dom import minidom
import xml.etree.ElementTree as ET
import os

#Place files to be modified in same directory as this python file.

xml_files = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".xml"):
            xml_files.append(file)
    break


for file in xml_files:
    to_remove=[]
    tree = ET.parse(file)
    root=tree.getroot()
    for elem in root:
        if elem.tag=='object':
            for elem2 in elem:
                if elem2.tag=='name' and elem2.text == 'dust':
                    to_remove.append(elem)
    for elem in to_remove:
        root.remove(elem)
    
    tree.write("modified/"+file)
        
        
