import cv2

from game import build_cover

if __name__ == '__main__':
    # num_rois = label_objects_in_image(path='data/test.jpg')
    # for i in range(num_rois):
    #     print(detect_web_objects(path=f'data/images/roi_{i}.png'))
    text = cv2.imread('data/text/res.jpg')
    roi = cv2.imread('data/images/roi_5.png')
    build_cover(text, roi)
    exit(0)
