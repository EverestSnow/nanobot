"""LLM request/response logging wrapper for litellm.acompletion."""

import json
from typing import Any, Dict
from litellm import acompletion

from loguru import logger


async def logged_acompletion(**kwargs: Any) -> Any:
    """
    Wrapper around litellm.acompletion that logs requests and responses.

    Args:
        **kwargs: Same arguments as litellm.acompletion

    Returns:
        The response from litellm.acompletion
    """
    # Prepare log data (sanitize sensitive info)
    request_log = {
        "model": kwargs.get("model"),
        "max_tokens": kwargs.get("max_tokens"),
        "temperature": kwargs.get("temperature"),
        "tools": kwargs.get("tools") is not None,
        "tool_choice": kwargs.get("tool_choice"),
        "messages_count": len(kwargs.get("messages", [])),
        # Truncate message content for logging
        "messages_preview": [
            {"role": msg["role"],
             # "content": msg["content"][:100] + "..." if len(msg.get("content", "")) > 100 else msg["content"]
             "content": msg["content"]
             }
            for msg in kwargs.get("messages", [])  # Log first 3 messages
            # for msg in kwargs.get("messages", [])[:3]  # Log first 3 messages
        ]
    }

    # Remove sensitive headers from logging
    if "extra_headers" in kwargs:
        headers = kwargs["extra_headers"].copy()
        # Mask common sensitive headers
        for key in headers:
            if any(sensitive in key.lower() for sensitive in ["key", "token", "auth"]):
                headers[key] = "***"
        request_log["extra_headers"] = headers

    logger.info(f"LLM Request: {json.dumps(request_log, ensure_ascii=False)}")

    try:
        response = await acompletion(**kwargs)

        # 记录原始响应（解析前）
        logger.debug("LLM Raw Response: {}", json.dumps(
            response.model_dump(exclude_none=True) if hasattr(response, "model_dump") else str(response),
            ensure_ascii=False, indent=2
        ))

        # Log response summary
        response_log = {
            "finish_reason": response.choices[0].finish_reason if response.choices else None,
            "content_length": len(response.choices[0].message.content or "") if response.choices else 0,
            "tool_calls": len(response.choices[0].message.tool_calls) if (
                    response.choices and
                    hasattr(response.choices[0].message, "tool_calls") and
                    response.choices[0].message.tool_calls
            ) else 0,
        }

        # Log usage if available
        if hasattr(response, "usage") and response.usage:
            response_log["usage"] = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        logger.info(f"LLM Response: {json.dumps(response_log, ensure_ascii=False)}")
        return response

    except Exception as e:
        logger.error(f"LLM Error: {str(e)}")
        raise