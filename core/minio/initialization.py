from minio import Minio

from core.logger import logger
from core.settings import settings


class MinioClient:
    _client: Minio | None = None

    @classmethod
    async def init_minio(cls) -> None:
        if cls._client is not None:
            logger.error("Minio is already initialized")
            return None

        cls._client = Minio(
            settings.minio_url,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure
        )
        logger.info("Minio initialized")

    @classmethod
    async def close_minio(cls) -> None:
        if cls._client is not None:
            logger.info("Minio closed")
            cls._client = None

    @classmethod
    def get_minio(cls) -> Minio:
        return cls._client
