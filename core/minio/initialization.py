from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session

from core.logger import logger
from core.settings import settings


class MinioClient:
    _client: AioBaseClient | None = None

    @classmethod
    async def init_minio(cls) -> None:
        if cls._client is not None:
            logger.error("Minio is already initialized")
            return None

        session = get_session()
        cls._client = session.create_client(
            's3',
            endpoint_url=settings.minio_url,
            aws_secret_access_key=settings.minio_secret_key,
            aws_access_key_id=settings.minio_access_key,
            region_name='us-east-1'
        )
        logger.info("Minio initialized")

        async with cls._client as client:
            try:
                response = await client.list_buckets()
                if 'Buckets' in response:
                    buckets = [bucket['Name'] for bucket in response['Buckets']]
                    if settings.minio_bucket not in buckets:
                        await client.create_bucket(Bucket=settings.minio_bucket)
                        logger.info("Bucket created")
                    else:
                        logger.info("Bucket already exists")
            except Exception as e:
                logger.error(f"Error creating bucket: {e}")

    @classmethod
    async def close_minio(cls) -> None:
        if cls._client is not None:
            logger.info("Minio closed")
            cls._client = None

    @classmethod
    def get_minio(cls) -> AioBaseClient:
        return cls._client
