import cv2
import math
import numpy as np
from google.cloud import vision


def get_image_objects(path):
    vision_client = vision.ImageAnnotatorClient()
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    annotations = vision_client.object_localization(image=image).localized_object_annotations
    return annotations


def label_objects_in_image(path):
    objects = get_image_objects(path=path)
    image = cv2.imread(path)
    height, width, _ = image.shape
    for obj in objects:
        vertices = list(obj.bounding_poly.normalized_vertices)
        polygon = [(math.floor(width * vtx.x), math.floor(height * vtx.y)) for vtx in vertices]
        np_polygon = np.array(polygon, np.int32)
        cv2.polylines(image, [np_polygon], True, (36, 255, 12), 2)
        cv2.putText(image, obj.name, polygon[-1], cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)
    image = cv2.resize(image, (1280, 720), interpolation=cv2.INTER_AREA)

    cv2.imshow('image', image)
    cv2.waitKey()
