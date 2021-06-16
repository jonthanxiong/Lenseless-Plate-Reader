import os

#Place xml files to be compiled in same directory as this python file.

xml_files = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".xml"):
            xml_files.append(file)
    break

print("Total xml files: " + str(len(xml_files)))

with open("file_names.txt","w") as f:
    for file in xml_files:
        f.write(file.split('.')[0]+'\n')

