import cv2
import math
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
    original = image.copy()
    height, width, _ = image.shape
    for i, obj in enumerate(objects):
        vertices = list(obj.bounding_poly.normalized_vertices)
        polygon = [(math.floor(width * vtx.x), math.floor(height * vtx.y)) for vtx in vertices]
        cv2.rectangle(image, polygon[0], polygon[2], (36, 255, 12), 2)
        cv2.putText(image, obj.name, polygon[-1], cv2.FONT_HERSHEY_SIMPLEX, 1, (36, 255, 12), 2)
        roi = original[polygon[0][1]:polygon[2][1], polygon[0][0]:polygon[2][0]]
        cv2.imwrite(f'data/images/roi_{i}.png', roi)
    # image = cv2.resize(image, (1280, 720), interpolation=cv2.INTER_AREA)
    # cv2.imshow('image', image)
    # cv2.waitKey()
    return len(objects)


def detect_web_objects(path):
    vision_client = vision.ImageAnnotatorClient()
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.web_detection(image=image)
    annotations = response.web_detection
    labels = sorted(annotations.web_entities, key=lambda l: -l.score)
    result = {
        'all_labels': [(we.description, we.score) for we in labels if we.description],
        'best_guesses': [g.label for g in annotations.best_guess_labels]
    }
    return result
