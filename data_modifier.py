import os
import xml.etree.ElementTree as ET

from random import randrange
from shutil import copyfile

# file type is for example: '.jpg' or '.txt'
def get_all_files_from_directory(directory_path, file_type):
    files_of_type = []

    for _, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(file_type):
                files_of_type.append(file)
        break

    return files_of_type

# counts number of objects in annotations from a directory
# annotations need to be in voc format
def count_annotated_objects(annotations_path, objects_to_count={"bead"}):
    objects = dict()
    for object in objects_to_count:
        objects[object] = 0

    xml_files = get_all_files_from_directory(annotations_path, ".xml")

    for file in xml_files:
        tree = ET.parse(os.path.join(annotations_path, file))
        root = tree.getroot()
        for elem in root:
            if elem.tag == 'object':
                for elem2 in elem:
                    if elem2.tag == 'name' and elem2.text in objects_to_count:
                        objects[elem2.text] += 1

    total_objects = 0
    for object in objects_to_count:
        total_objects += objects[object]
        print(object + "objects: " + str(objects[object]))
    print("total objects: " + str(total_objects))

# reformat voc annotations from senseai website
# if annotations_path and processed_directory_path are the same, original xml files are overwritten
def reformatter(annotations_path, processed_directory_path='reformatted/'):
    if not os.path.exists(processed_directory_path):
        os.mkdir(processed_directory_path)

    xml_files = get_all_files_from_directory(annotations_path, ".xml")

    for file in xml_files:
        lines = None
        with open(os.path.join(annotations_path, file)) as f:
            lines = f.read().splitlines()
        with open(os.path.join(processed_directory_path, file), "w") as f:
            f.write("<annotation>\n")
            f.write("\t<filename>" + file.split(".")[0] + ".jpg" + "</filename>\n")
            f.write("\t<folder>cells</folder>\n")
            f.write("\t<source>\n")
            f.write("\t\t<database>cells</database>\n")
            f.write("\t\t<annotation>custom</annotation>\n")
            f.write("\t\t<image>custom</image>\n")
            f.write("\t</source>\n")

            found = 0
            for line in lines:
                if found == 4:
                    f.write(line + "\n")
                    break
                if found == 3:
                    found += 1
                    f.write(line.split("3")[0] + "1" + line.split("3")[1] + "\n")
                if found > 0 and found < 3:
                    found += 1
                    f.write(line + "\n")
                if "<size>" in line:
                    found = 1
                    f.write(line + "\n")

            f.write("\t<segmented>0</segmented>\n")

            found = False
            for line in lines:
                if not found and "<object>" in line:
                    found = True
                if found:
                    if "<pose>" in line:
                        f.write(line.split("Unspecified")[0] + "unspecified" + line.split("Unspecified")[1] + "\n")
                    elif "<truncated>" in line or "<difficult>" in line:
                        f.write(line.split("Unspecified")[0] + "0" + line.split("Unspecified")[1] + "\n")
                    elif "</annotation>" in line:
                        f.write(line)
                    else:
                        f.write(line + "\n")

def compile_annotation_file_names(annotations_path):
    xml_files = get_all_files_from_directory(annotations_path, ".xml")

    return {file.split('.')[0] for file in xml_files}

# existing annotations can be acquired through the previous function: compile_annotation_file_names
def remove_unannotated_images(images_path, existing_annotations, display_message=False):
    image_files = get_all_files_from_directory(images_path, ".jpg")

    removed_count = 0
    for file in image_files:
        if file.split('.')[0] not in existing_annotations:
            os.remove(os.path.join(images_path, file))
            removed_count += 1

    if display_message:
        print("Total JPG Files: " + str(len(image_files)))
        print("Total xml Files: " + str(len(existing_annotations)))
        print("JPG Files Removed: " + str(removed_count))

# if annoations_path and processed_directory_path are the same, then the original xml files are overwritten
def annotated_object_remover(annotations_path, processed_directory_path=os.path.join("modified_objects/"), objects_to_remove={"dust"}):
    if not os.path.exists(processed_directory_path):
        os.mkdir(processed_directory_path)

    xml_files = get_all_files_from_directory(annotations_path, ".xml")

    for file in xml_files:
        to_remove = []
        tree = ET.parse(os.path.join(annotations_path, file))
        root = tree.getroot()
        for elem in root:
            if elem.tag == 'object':
                for elem2 in elem:
                    if elem2.tag == 'name' and elem2.text in objects_to_remove:
                        to_remove.append(elem)

        for elem in to_remove:
            root.remove(elem)

        tree.write(os.path.join(processed_directory_path, file))

def find_average_object_sizes(annotations_path):
    xml_files = get_all_files_from_directory(annotations_path, ".xml")

    total_area = 0
    total_height = 0
    total_width = 0
    total_objects = 0

    for file in xml_files:
        tree = ET.parse(os.path.join(annotations_path, file))
        root = tree.getroot()

        for elem in root.iter('object'):
            for elem2 in elem:
                if elem2.tag == 'bndbox':
                    width = int(elem2[2].text) - int(elem2[0].text)
                    height = int(elem2[3].text) - int(elem2[1].text)
                    total_area += width * height
                    total_height += height
                    total_width += width
            total_objects += 1

    print("Average Area: " + str(total_area / total_objects))
    print("Average Width: " + str(total_width / total_objects))
    print("Average Height: " + str(total_height / total_objects))


def generate_training_set(images_path, annotations_path, training_set=os.path.join("training_set/"), test_percentage=.1, labels=['bead']):
    if not os.path.exists(training_set):
        os.mkdir(training_set)
    if not os.path.exists(os.path.join(training_set,"Annotations")):
        os.mkdir(os.path.join(training_set, "Annotations"))
    if not os.path.exists(os.path.join(training_set, "ImageSets")):
        os.mkdir(os.path.join(training_set,"ImageSets"))
    if not os.path.exists(os.path.join(training_set,"ImageSets/Main")):
        os.mkdir(os.path.join(training_set, "ImageSets/Main"))
    if not os.path.exists(os.path.join(training_set, "JPEGImages")):
        os.mkdir(os.path.join(training_set, "JPEGImages"))

    with open(os.path.join(training_set, "labels.txt")) as f:
        f.write('\n'.join(labels))

    annotation_files = get_all_files_from_directory(annotations_path, ".xml")
    image_files = get_all_files_from_directory(images_path, ".jpg")

    for file in annotation_files:
        copyfile(annotations_path + file, os.path.join(training_set, "Annotations/"+file))
    for file in image_files:
        copyfile(images_path + file, os.path.join(training_set, "JPEGImages/"+file))

    file_names = compile_annotation_file_names(annotations_path)

    test_set = set()
    test_number = int(len(file_names) * test_percentage)
    val_set = set()
    val_number = test_number
    output_dir=os.path.join(training_set,"ImageSets/Main")

    for i in range(test_number):
        test_set.add(file_names.pop(randrange(len(file_names))))
    test_set = sorted(list(test_set))
    with open(output_dir + "test.txt", "w") as f:
        f.write('\n'.join(test_set))

    for i in range(val_number):
        val_set.add(file_names.pop(randrange(len(file_names))))
    val_set = sorted(list(val_set))
    with open(output_dir + "val.txt", "w") as f:
        f.write('\n'.join(val_set))

    train_set = sorted(file_names)
    with open(output_dir + "train.txt", 'w') as f:
        f.write('\n'.join(train_set))

    trainval_set = train_set.copy()
    trainval_set.extend(val_set)
    with open(output_dir + "trainval.txt", "w") as f:
        f.write('\n'.join(trainval_set))




