import cv2

from discovery import DiscoveryClient
from game import build_cover, process_game
from upload import upload_image

if __name__ == '__main__':
    # num_rois = label_objects_in_image(path='data/test.jpg')
    # for i in range(num_rois):
    #     print(detect_web_objects(path=f'data/images/roi_{i}.png'))
    # text = cv2.imread('data/text/res.jpg')
    # roi = cv2.imread('data/images/roi_5.png')
    # build_cover(text, roi)
    client = DiscoveryClient()
    games = client.all_documents()
    process_game(games[0])
    exit(0)
