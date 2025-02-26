from minio import Minio
from minio.error import S3Error
from core.logger import logger
from core.settings import settings


class MinioClient:
    _client = None

    @classmethod
    def init_minio(cls) -> None:
        if cls._client is not None:
            logger.error("Minio is already initialized")
            return None

        cls._client = Minio(
            settings.minio_url,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure
        )
        cls.create_bucket(settings.minio_bucket)
        logger.info("Minio initialized")

    @classmethod
    def create_bucket(cls, bucket_name: str) -> None:
        if cls._client is None:
            raise ValueError("Minio client is not initialized. Call 'init_minio' first.")

        try:
            if not cls._client.bucket_exists(bucket_name):
                cls._client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' created")
            else:
                logger.info(f"Bucket '{bucket_name}' already exists")
        except S3Error as e:
            logger.error(f"Error creating bucket '{bucket_name}': {e}")

    @classmethod
    def close_minio(cls) -> None:
        if cls._client is not None:
            cls._client = None
            logger.info("Minio closed")

    @classmethod
    def get_minio(cls):
        return cls._client
