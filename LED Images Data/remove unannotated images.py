import os

#place this python file into folder with jpg images
#place a file called file_names.txt listing existing xml files
#this program removes jpgs that don't have a corresponding or existing xml

jpg_files = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".jpg"):
            jpg_files.append(file)
    break

with open("file_names.txt","r") as f:
    existing_files=set(f.read().split('\n')[:-1])

removed_count = 0
for file in jpg_files:
    if file.split('.')[0] not in existing_files:
        os.remove(file)
        removed_count+=1

print("Total JPG Files: " + str(len(jpg_files)))
print("Total xml Files: " + str(len(existing_files)))
print("JPG Files Removed: " + str(removed_count))
    

