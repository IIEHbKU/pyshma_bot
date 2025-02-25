import random

import cv2

from core.redis.access import get_redis
from core.roboflow.access import get_roboflow
from gateway.redis import get_color_from_redis, store_color_in_redis


async def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    return image


def get_random_contrast_color():
    return random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)


async def draw_bounding_boxes(redis_client, image, boxes):
    for box in boxes:
        x, y, w, h = int(box['x'] - box['width'] / 2), int(box['y'] - box['height'] / 2), int(box['width']), int(
            box['height'])
        confidence = box['confidence']

        label = box['class']
        color = await get_color_from_redis(redis_client, label)
        if color is None:
            color = get_random_contrast_color()
            await store_color_in_redis(redis_client, label, color)

        cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)

        text = f"{label}: {int(confidence * 100)}%"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_TRIPLEX, 0.3, 1)
        cv2.rectangle(image, (x, y - text_height - 5), (x + text_width, y), color, -1)
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_TRIPLEX, 0.3, (255, 255, 255), 1)


async def main():
    roboflow_client = await get_roboflow()
    redis_client = await get_redis()

    image_file = "../img.png"
    image = cv2.imread(image_file)

    max_width = 800
    max_height = 800
    image = await resize_image(image, max_width, max_height)
    result = await roboflow_client.infer_async(image, model_id="samolet-init/1")
    print(result)

    if 'predictions' in result:
        await draw_bounding_boxes(redis_client, image, result['predictions'])
        output_file = "../img_with_boxes.png"
        cv2.imwrite(output_file, image)
        print(f"Image with bounding boxes saved to {output_file}")
    else:
        print("No predictions found in the result.")
