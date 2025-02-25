from minio import Minio

from core.minio.initialization import MinioClient


async def get_minio() -> Minio:
    return MinioClient.get_minio()
