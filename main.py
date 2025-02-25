import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from core.redis.initialization import RedisClient
from core.roboflow.initialization import RoboflowClient
from core.settings import settings
from core.postgres.initialization import PostgresClient
from core.minio.initialization import MinioClient
from core.logger import logger
from handlers import include_routers


async def shutdown(bot: Bot):
    await PostgresClient.close_postgres()
    await RedisClient.close_redis()
    await MinioClient.close_minio()
    await RoboflowClient.close_roboflow()
    await bot.session.close()
    logger.info("Bot and all resources have been successfully closed")


async def main():
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode="html"))
    dp = Dispatcher(storage=MemoryStorage())
    include_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await PostgresClient.init_postgres()
        await RedisClient.init_redis()
        await MinioClient.init_minio()
        await RoboflowClient.init_roboflow()
        await dp.start_polling(bot)
        logger.info("Bot and all resources have been successfully started")
    except asyncio.exceptions.CancelledError:
        logger.info("The polling cycle was interrupted")
    finally:
        await shutdown(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
