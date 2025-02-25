import os

import aiofiles
import cv2

from core.minio.access import get_minio
from core.redis.access import get_redis
from core.roboflow.access import get_roboflow
from core.settings import settings
from utils.generate_bounding_boxes import generate_bounding_boxes
from utils.generate_txt_file import generate_txt_report


async def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    return image


async def create_report(folder, image_url, reports_count):
    reports_count += 1

    roboflow_client = await get_roboflow()
    redis_client = await get_redis()
    minio_client = await get_minio()

    image = cv2.imread(image_url)
    image = await resize_image(image, 1000, 1000)

    result = await roboflow_client.infer_async(image, model_id=settings.roboflow_model_id)

    filename_txt = await generate_txt_report(folder, reports_count, result)
    async with aiofiles.open(filename_txt, 'r') as text_file:
        text_data = await text_file.read()
    await minio_client.put_object(
        Bucket=settings.minio_bucket,
        Key=f"{folder}/{os.path.basename(filename_txt)}",
        Body=text_data.encode('utf-8'),
        ContentType='text/plain'
    )

    if 'predictions' in result:
        filename_png = generate_bounding_boxes(redis_client, image, reports_count, result['predictions'])
        async with aiofiles.open(filename_png, 'rb') as image_file:
            image_data = await image_file.read()
        await minio_client.put_object(
            Bucket=settings.minio_bucket,
            Key=f"{folder}/{os.path.basename(filename_png)}",
            Body=image_data,
            ContentType='image/png'
        )
        os.remove(filename_png)
    else:
        async with aiofiles.open(image_url, 'rb') as image_file:
            image_data = await image_file.read()
        await minio_client.put_object(
            Bucket=settings.minio_bucket,
            Key=f"{folder}/{os.path.basename(image_url)}",
            Body=image_data,
            ContentType='image/png'
        )

    os.remove(image_url)
    os.remove(filename_txt)
