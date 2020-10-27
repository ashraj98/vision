import cv2
import numpy as np


def find_bounding_boxes(path):
    image = cv2.imread(path)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_filtered = cv2.bilateralFilter(gray, 7, 50, 50)
    # blurred = cv2.medianBlur(gray, 9)
    edges = cv2.Canny(gray_filtered, 50, 100)
    # create a kernel
    morph_kernel_size = 5
    kernel = np.ones((morph_kernel_size, morph_kernel_size))
    # do a morphological close
    res = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    # cv2.floodFill(res, None, (0, 0), 255)
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('image', res)
    cv2.waitKey()

    ROI_number = 0
    contours = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        # ROI = original[y:y+h, x:x+w]
        # cv2.imwrite(f'data/images/ROI_{ROI_number}.png', ROI)
        # ROI_number += 1

    cv2.imshow('image', image)
    cv2.waitKey()


def remove_background(path):
    image = cv2.imread(path)
    backSub = cv2.createBackgroundSubtractorKNN()
    fgMask = backSub.apply(image)
    cv2.imshow('Frame', image)
    cv2.waitKey()
    cv2.imshow('FG Mask', fgMask)
    cv2.waitKey()
