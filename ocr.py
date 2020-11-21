import sys

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
    roi = img[max_poly[0][1]:max_poly[2][1], max_poly[0][0]:max_poly[2][0]]
    cv2.imwrite('data/text/res.jpg', roi)
    return True


def remove_text_background(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    sh, sw = gray.shape
    edge_color =\
        (np.sum(gray[0:, 0]) + np.sum(gray[0, 0:]) + np.sum(gray[0:, sw-1]) + np.sum(gray[sh-1, 0:])) / ((sh + sw) * 2)
    print(edge_color)
    pad_color = 0 if edge_color else 255
    border_size = 10
    bordered = cv2.copyMakeBorder(
        blurred,
        top=border_size,
        bottom=border_size,
        left=border_size,
        right=border_size,
        borderType=cv2.BORDER_CONSTANT,
        value=pad_color
    )
    # ret, thresh = cv2.threshold(bordered, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.adaptiveThreshold(bordered, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(thresh, 50, 100)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    h, w = bordered.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    # Flood fill from point (0, 0)
    cv2.floodFill(close, mask, (0, 0), 255)
    no_border = close[border_size:h-border_size, border_size:w-border_size]
    rgb = cv2.cvtColor(no_border, cv2.COLOR_GRAY2RGB)
    text_only = cv2.subtract(image, rgb)
    cv2.imshow('result', text_only)
    cv2.waitKey()
