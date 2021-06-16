import xml.etree.ElementTree as ET
import os

#Place files to be sliced in same directory as this python file.

xml_files = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".xml"):
            xml_files.append(file)
    break

if not os.path.exists("sliced_annotations"):
    os.mkdir("sliced_annotations")

image_width=3864
image_height=2080

average_area = 8026

image_division=7

new_image_width=image_width//image_division
new_image_height=image_height//image_division

for file in xml_files:
    file_name = file.split(".")[0]

    for i in range(image_division**2):       
        image_row=i//image_division
        image_col=i%image_division
        image_xmin=new_image_width*image_col
        image_xmax=new_image_width*(image_col+1)-1
        image_ymin=new_image_height*image_row
        image_ymax=new_image_height*(image_row+1)-1

        tree = ET.parse(file)
        root=tree.getroot()

        to_remove = []
        
        for elem in root.iter('object'):
            for elem2 in elem:
                if elem2.tag=='bndbox':
                    if int(elem2[0].text)>image_xmax or int(elem2[1].text)>image_ymax \
                        or int(elem2[2].text)<image_xmin or int(elem2[3].text)<image_ymin:
                            to_remove.append(elem)
                    else:
                        if int(elem2[0].text)<image_xmin:
                            elem2[0].text=str(image_xmin)
                        if int(elem2[1].text)<image_ymin:
                            elem2[1].text=str(image_ymin)
                        if int(elem2[2].text)>image_xmax:
                            elem2[2].text=str(image_xmax)
                        if int(elem2[3].text)>image_ymax:
                            elem2[3].text=str(image_ymax)
                            
                        elem2[0].text=str(int(elem2[0].text)-image_xmin)
                        elem2[1].text=str(int(elem2[1].text)-image_ymin)
                        elem2[2].text=str(int(elem2[2].text)-image_xmin)
                        elem2[3].text=str(int(elem2[3].text)-image_ymin)

                        object_width = int(elem2[2].text)-int(elem2[0].text)
                        object_height = int(elem2[3].text)-int(elem2[1].text)
                        object_area = object_width * object_height

                        if object_area < (.3 * average_area):
                            to_remove.append(elem)


        for elem in to_remove:
            root.remove(elem)
        if len(tree.findall('object'))!=0:
            tree.find("filename").text = file_name + "-" +str(i)+".jpg"
            tree.find("size").find("width").text = str(new_image_width)
            tree.find("size").find("height").text = str(new_image_height)
            tree.write("sliced_annotations/"+file_name + "-" +str(i)+".xml")

                   
                        


                        
            
            
