import os
import os.path as path
import xml.etree.ElementTree as ET
from glob import glob

LABEL_FORMAT = "*.xml"
ROOT_PATH = "../../DATASET/DETRAC"
TRAIN_LABEL_DIR = "DETRAC-Train-Annotations-XML"
TRAIN_LABEL_PATH = path.join(ROOT_PATH, TRAIN_LABEL_DIR)
LABEL_XMLS = glob(path.join(TRAIN_LABEL_PATH, LABEL_FORMAT))

class_list = ['car', 'bus', 'van']


# [class] [identity] [x_center] [y_center] [width] [height]
def extract_traget_info(target):
    width = None
    left = None
    top = None
    height = None
    vechicle_type = None
    id = target.attrib["id"]
    for item in target:
        if item.tag == "box":
            box = item.attrib
            left = float(box["left"])
            top = float(box["top"])
            width = float(box["width"])
            height = float(box["height"])

        if item.tag == "attribute":
            attribute = item.attrib
            vechicle_type = attribute["vehicle_type"]
    if vechicle_type == 'others':
        class_idx = -1
    else:
        class_idx = class_list.index(vechicle_type)
    x_center = left + (width / 2.0)
    y_center = top + (height / 2.0)
    str_result = "{} {} {} {} {} {}".format(class_idx, id, x_center, y_center, width, height)
    return str_result


def read_frame_tag(frame_tag):
    str_label = []
    for target_list in frame_tag:

        for target in target_list:
            target_info = extract_traget_info(target)
            str_label.append(target_info)
    return "\n".join(str_label)

for xml_file in LABEL_XMLS:
    print("Reading {}".format(xml_file))
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for elem in root:
        if elem.tag == "frame":
            string_frame = read_frame_tag(elem)
            print(string_frame)
        print("----------------")
    break
