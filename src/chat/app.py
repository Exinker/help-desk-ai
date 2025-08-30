import logging
from collections.abc import Mapping, Sequence

import chainlit as cl

from chat.service import Service
from config import CHAT_CONFIG

LOGGER = logging.getLogger(__name__)


@cl.on_chat_start
async def on_chat_start():
    service = Service.create(
        knowledge_base_id=CHAT_CONFIG.knowledge_base_id,
        system_prompt=CHAT_CONFIG.system_prompt,
        retrieve_prompt=CHAT_CONFIG.retrieve_prompt,
        k=CHAT_CONFIG.k,
    )
    cl.user_session.set('service', service)

    cl.user_session.set('history', [])


@cl.on_message
async def on_message(request: cl.Message) -> cl.Message:
    service: Service = cl.user_session.get('service')
    history: Sequence[Mapping[str, str]] = cl.user_session.get('history')

    LOGGER.warning(history)
    LOGGER.warning(request.content)

    response = cl.Message(content='')
    try:
        async for chunk in service.retrieve_chain.astream({'question': request.content, 'history': history}):
            await response.stream_token(chunk)
        await response.send()
    finally:
        history.extend((
            {'user': request.content},
            {'assistant': response.content},
        ))
