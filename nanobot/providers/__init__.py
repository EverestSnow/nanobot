"""LLM provider abstraction module."""

from nanobot.providers.base import LLMProvider, LLMResponse
from nanobot.providers.litellm_provider import LiteLLMProvider

__all__ = ["LLMProvider", "LLMResponse", "LiteLLMProvider"]

from loguru import logger
import sys

# Remove default handler
# logger.remove()

# Add console handler
# logger.add(sys.stdout, level="INFO")

# Add file handler for LLM logs
logger.add(
    # "~/.nanobot/logs/llm.log",
    "logs/llm_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    # filter=lambda record: "LLM" in record["message"],
    enqueue=True,  # 异步写入
)