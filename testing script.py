import os

from image_processor import Image_Processor
from data_modifier import *

ImageP = Image_Processor()
ImageP.combine_sliced_overlap_images("sliced_overlap_images")

