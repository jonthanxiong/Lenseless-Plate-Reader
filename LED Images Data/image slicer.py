from PIL import Image
import os

#Place images to be sliced in same directory as this python file.

images = []

for _,_,files in os.walk("."):
    for file in files:
        if file.endswith(".jpg"):
            images.append(file)
    break

if not os.path.exists("sliced_images"):
    os.mkdir("sliced_images")

image_width=3864
image_height=2180

image_division=7

new_image_width=image_width//image_division
new_image_height=image_height//image_division

for image in images:
    image_name = image.split(".")[0]
    im = Image.open(image)

    for i in range(image_division**2):
        image_row=i//image_division
        image_col=i%image_division
        image_xmin=new_image_width*image_col
        image_xmax=new_image_width*(image_col+1)-1
        image_ymin=new_image_height*image_row
        image_ymax=new_image_height*(image_row+1)-1

        cropim=im.crop((image_xmin,image_ymin,image_xmax,image_ymax))

        cropim.save("sliced_images/"+image_name+"-"+str(i)+".jpg")

        
