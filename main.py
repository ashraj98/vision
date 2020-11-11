from datetime import datetime

import requests

from discovery import DiscoveryClient
from game import process_game


def check_game_processed(game_slug):
    response = requests.get(f'http://localhost:8000/covers/?game={game_slug}')
    matches = response.json()
    return len(matches) > 0


if __name__ == '__main__':
    # num_rois = label_objects_in_image(path='data/test.jpg')
    # for i in range(num_rois):
    #     print(detect_web_objects(path=f'data/images/roi_{i}.png'))
    # text = cv2.imread('data/text/res.jpg')
    # roi = cv2.imread('data/images/roi_5.png')
    # build_cover(text, roi)
    client = DiscoveryClient()
    games = client.all_documents()
    print(f"Started at {datetime.now().strftime('%H:%M:%S')}")
    for i, game in enumerate(games):
        if not check_game_processed(game['slug']):
            process_game(game)
            print(f"#{i + 1}: Processed {game['name']} at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"#{i + 1}: Skipped {game['name']} at {datetime.now().strftime('%H:%M:%S')}")
    exit(0)
