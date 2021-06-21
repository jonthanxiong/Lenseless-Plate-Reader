import os

from image_processor import Image_Processor
from data_modifier import *


ImageP = Image_Processor()


# Below section is to prep images for training
ImageP.slice_overlap_images(os.path.join("Images_for_Training_Directory"))


# Below section is to prep annotation data for training
# reformatter can only be run once on the annotation. Comment out the reformatter function if you want to rerun this code
reformatter("Annotations_for_Training_Directory")
annotated_object_remover(os.path.join("reformatted"))
ImageP.slice_overlap_annotations(os.path.join("modified_objects"))


# Below section is to generate training information
generate_training_set(os.path.join("sliced_overlap_images"), os.path.join("sliced_overlap_annotations"))


#Below section is code to combine sliced images back into whole image
ImageP.combine_sliced_overlap_images("tested_images")

