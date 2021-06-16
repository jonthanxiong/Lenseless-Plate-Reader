from PIL import Image
import os


#Place images to be combined in same directory as this python file.

image_file_names = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".jpg"):
            image_file_names.append(file)
    break

if not os.path.exists("combined_images"):
    os.mkdir("combined_images")

images_per_axis=7
images = dict()

for file_name in image_file_names:
    name=file_name.split('.')[0].split('-')[0]
    image_part=int(file_name.split('.')[0].split('-')[1])
    if name not in images:
        images[name]=list(range(images_per_axis**2))
    images[name][image_part]=Image.open(file_name)


images_sizes=[images[name][0].size for name in images.keys()]
combined_images=list()
for w,h in images_sizes:
    combined_images.append(Image.new('RGB',(images_per_axis*w,images_per_axis*h)))
for i,image in enumerate(combined_images):
    image_parts=images[list(images.keys())[i]]
    count=0
    for j in range(images_per_axis):
        for k in range(images_per_axis):
            image.paste(image_parts[count],(k*images_sizes[i][0],j*images_sizes[i][1]))
            count+=1
    image.save("combined_images/merged"+list(images.keys())[i]+".jpg","JPEG")
