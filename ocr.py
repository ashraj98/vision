import cv2
from google.cloud import vision
import io
import numpy as np


def extract_text_from_image(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    img = cv2.imread(path)

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    max_area = 0
    max_poly = None
    for text in texts:
        vertices = list(text.bounding_poly.vertices)
        polygon = [(vtx.x, vtx.y) for vtx in vertices]
        cur_max = (polygon[2][0] - polygon[0][0]) * (polygon[2][1] - polygon[0][1])
        if cur_max > max_area:
            max_area = cur_max
            max_poly = polygon

    if max_poly is None:
        return False
    cv2.rectangle(img, max_poly[0], max_poly[2], (36, 255, 12), 2)
    roi = img[max_poly[0][1]:max_poly[2][1], max_poly[0][0]:max_poly[2][0]]
    cv2.imwrite('data/text/res.jpg', roi)
    return True


def remove_text_background(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    edges = cv2.Canny(blurred, 50, 100)
    morph_kernel_size = 4
    kernel = np.ones((morph_kernel_size, morph_kernel_size))
    # do a morphological close
    res = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('result', res)
    cv2.waitKey()
