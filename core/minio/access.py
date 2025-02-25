from aiobotocore.client import AioBaseClient

from core.minio.initialization import MinioClient


async def get_minio() -> AioBaseClient:
    return MinioClient.get_minio()
