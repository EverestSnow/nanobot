"""
nanobot - A lightweight AI agent framework
"""

__version__ = "0.1.4"
__logo__ = "🐈"

from loguru import logger
import sys

# 移除默认控制台处理器（可选）
logger.remove()

# 添加控制台输出（可选）
# logger.add(sys.stderr, level="INFO")

# 添加文件输出（按日期轮转，保留 7 天）
logger.add(
    "logs/nanobot_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # 每天午夜轮转
    retention="7 days",  # 保留 7 天
    level="DEBUG",  # 记录 DEBUG 及以上
    enqueue=True,  # 异步写入
)