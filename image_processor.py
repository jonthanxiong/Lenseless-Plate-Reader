import os
import xml.etree.ElementTree as ET
from data_modifier import *

from PIL import Image

class Image_Processor():

    def __init__(self, image_width = 3864, image_height = 2180, average_object_area = 8026, image_division = 7):
        self._original_image_width = image_width
        self._original_image_height = image_height
        self._new_image_width = image_width // image_division
        self._new_image_height = image_height // image_division
        self._average_object_area = average_object_area
        self._image_division = image_division

    # slices an annotation into self._image_division**2 parts
    # annotations need to be in voc format
    def slice_annotations(self, annotations_path, processed_directory_path="sliced_annotations/"):
        if not os.path.exists(processed_directory_path):
            os.mkdir(processed_directory_path)

        xml_files = get_all_files_from_directory(annotations_path, ".xml")

        for file in xml_files:
            file_name = file.split(".")[0]

            for i in range(self._image_division ** 2):
                image_row = i // self._image_division
                image_col = i % self._image_division
                image_xmin = self._new_image_width * image_col
                image_xmax = self._new_image_width * (image_col + 1) - 1
                image_ymin = self._new_image_height * image_row
                image_ymax = self._new_image_height * (image_row + 1) - 1

                tree = ET.parse(os.path.join(annotations_path, file))
                root = tree.getroot()

                to_remove = []

                for elem in root.iter('object'):
                    for elem2 in elem:
                        if elem2.tag == 'bndbox':
                            if int(elem2[0].text) > image_xmax or int(elem2[1].text) > image_ymax \
                                    or int(elem2[2].text) < image_xmin or int(elem2[3].text) < image_ymin:
                                to_remove.append(elem)
                            else:
                                if int(elem2[0].text) < image_xmin:
                                    elem2[0].text = str(image_xmin)
                                if int(elem2[1].text) < image_ymin:
                                    elem2[1].text = str(image_ymin)
                                if int(elem2[2].text) > image_xmax:
                                    elem2[2].text = str(image_xmax)
                                if int(elem2[3].text) > image_ymax:
                                    elem2[3].text = str(image_ymax)

                                elem2[0].text = str(int(elem2[0].text) - image_xmin)
                                elem2[1].text = str(int(elem2[1].text) - image_ymin)
                                elem2[2].text = str(int(elem2[2].text) - image_xmin)
                                elem2[3].text = str(int(elem2[3].text) - image_ymin)

                                object_width = int(elem2[2].text) - int(elem2[0].text)
                                object_height = int(elem2[3].text) - int(elem2[1].text)
                                object_area = object_width * object_height

                                if object_area < (.3 * self._average_area):
                                    to_remove.append(elem)

                for elem in to_remove:
                    root.remove(elem)

                if len(tree.findall('object')) != 0:
                    tree.find("filename").text = file_name + "-" + str(i) + ".jpg"
                    tree.find("size").find("width").text = str(self._new_image_width)
                    tree.find("size").find("height").text = str(self._new_image_height)
                    tree.write(os.path.join(processed_directory_path, file_name + "-" + str(i) + ".xml"))

    # slices an image into self._image_division**2
    def slice_images(self, images_path, processed_directory_path='sliced_images/'):
        if not os.path.exists(processed_directory_path):
            os.mkdir(processed_directory_path)

        images = get_all_files_from_directory(images_path, ".jpg")

        # image_paths need to have format: hello/world.txt
        for image in images:
            image_name = image.split(".")[0]
            im = Image.open(os.path.join(images_path, image))

            for i in range(self._image_division ** 2):
                image_row = i // self._image_division
                image_col = i % self._image_division
                image_xmin = self._new_image_width * image_col
                image_xmax = self._new_image_width * (image_col + 1) - 1
                image_ymin = self._new_image_height * image_row
                image_ymax = self._new_image_height * (image_row + 1) - 1

                cropim = im.crop((image_xmin, image_ymin, image_xmax, image_ymax))

                cropim.save(os.path.join(processed_directory_path, image_name + "-" + str(i) + ".jpg"))

    # can combine sliced images from multiple image wells.
    # for ex.: can combine sliced images part of well image0019 and image0020 because function sorts by name
    def combine_sliced_images(self, images_path, processed_directory_path=os.path.join('combined_images/')):
        if not os.path.exists(processed_directory_path):
            os.mkdir(processed_directory_path)

        images = dict()
        image_file_names = get_all_files_from_directory(images_path)

        for file_name in image_file_names:
            name = file_name.split('.')[0].split('-')[0]
            image_part = int(file_name.split('.')[0].split('-')[1])
            if name not in images:
                images[name] = list(range(self._image_division ** 2))
            images[name][image_part] = Image.open(os.path.join(images_path, file_name))

        images_sizes = [images[name][0].size for name in images.keys()]
        combined_images = list()

        for w, h in images_sizes:
            combined_images.append(Image.new('RGB', (self._image_division * w, self._image_division * h)))

        for i, image in enumerate(combined_images):
            image_parts = images[list(images.keys())[i]]
            count = 0
            for j in range(self._image_division):
                for k in range(self._image_division):
                    image.paste(image_parts[count], (k * images_sizes[i][0], j * images_sizes[i][1]))
                    count += 1
            image.save(os.join.path(processed_directory_path, "/merged" + list(images.keys())[i] + ".jpg"), "JPEG")













