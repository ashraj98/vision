from gcloud import label_objects_in_image, detect_web_objects

if __name__ == '__main__':
    num_rois = label_objects_in_image(path='data/test.jpg')
    for i in range(num_rois):
        print(detect_web_objects(path=f'data/images/roi_{i}.png'))
    exit(0)
