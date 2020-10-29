from gcloud import get_image_objects, label_objects_in_image
from preprocess import find_bounding_boxes, remove_background

if __name__ == '__main__':
    label_objects_in_image(path='data/test.jpg')
    exit(0)
