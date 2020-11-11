import cv2
import requests
import numpy as np

from gcloud import label_objects_in_image, detect_web_objects
from ocr import extract_text_from_image
from upload import upload_image


def build_cover(text, roi):
    total_dim = (352, 264)
    text_padded = cv2.copyMakeBorder(text, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    roi_padded = cv2.copyMakeBorder(roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    text_shrink = max(text_padded.shape[0] / total_dim[0], text_padded.shape[1] / total_dim[1])
    if text_shrink > 1:
        text_dim = (int(text_padded.shape[1] / text_shrink), int(text_padded.shape[0] / text_shrink))
        final_text = cv2.resize(text_padded, text_dim, interpolation=cv2.INTER_AREA)
    else:
        final_text = text_padded
    roi_shrink = max(roi_padded.shape[0] / (total_dim[0] - final_text.shape[0]), roi_padded.shape[1] / total_dim[1])
    if roi_shrink > 1:
        roi_dim = (int(roi_padded.shape[1] / roi_shrink), int(roi_padded.shape[0] / roi_shrink))
        final_roi = cv2.resize(roi_padded, roi_dim, interpolation=cv2.INTER_AREA)
    else:
        final_roi = roi_padded
    text_width_start = (total_dim[1] - final_text.shape[1]) // 2
    final_image = np.zeros((total_dim[0], total_dim[1], 3), np.uint8)
    roi_width_start = (total_dim[1] - final_roi.shape[1]) // 2
    final_image[total_dim[0]-final_roi.shape[0]:, roi_width_start:roi_width_start+final_roi.shape[1]] = final_roi
    final_image[:final_text.shape[0], text_width_start:text_width_start+final_text.shape[1]] = final_text
    return final_image


def process_game(game):
    cover_url = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{game['cover']['image_id']}.jpg"
    r = requests.get(cover_url, allow_redirects=True)
    open('data/cover.jpg', 'wb').write(r.content)

    has_text = extract_text_from_image('data/cover.jpg')
    if has_text:
        text_img = cv2.imread('data/text/res.jpg')
    else:
        text_img = np.zeros((10, 20, 3), np.uint8)

    for idx, screenshot in enumerate(game['screenshots']):
        screenshot_url = f"https://images.igdb.com/igdb/image/upload/t_1080p/{screenshot['image_id']}.jpg"
        r = requests.get(screenshot_url, allow_redirects=True)
        open(f'data/screenshot{idx}.jpg', 'wb').write(r.content)
        num_rois = label_objects_in_image(path=f'data/screenshot{idx}.jpg')
        for i in range(num_rois):
            labels = detect_web_objects(path=f'data/images/roi_{i}.png')
            tags = [lbl[0] for lbl in labels['all_labels'] if lbl[1] > labels['all_labels'][0][1] * .65]
            tags.extend(labels['best_guesses'] * 5)
            roi_img = cv2.imread(f'data/images/roi_{i}.png')
            final_cover = build_cover(text_img, roi_img)
            cv2.imwrite('data/cover.jpg', final_cover)
            uid = upload_image('data/cover.jpg')
            for tag in tags:
                requests.post('http://localhost:8000/covers/', data={
                    'game': game['slug'],
                    'image': uid,
                    'tag': tag,
                    'size': roi_img.shape[0] * roi_img.shape[1]
                })
