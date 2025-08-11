import logging

import chainlit as cl

from chat.service import Service
from config import CHAT_CONFIG

LOGGER = logging.getLogger(__name__)


@cl.on_chat_start
async def on_chat_start():
    service = Service.create(
        knowledge_base_id=CHAT_CONFIG.knowledge_base_id,
        system_prompt=CHAT_CONFIG.system_prompt,
        k=CHAT_CONFIG.k,
    )
    cl.user_session.set('service', service)


@cl.on_message
async def on_message(message: cl.Message) -> cl.Message:
    service: Service = cl.user_session.get('service')

    LOGGER.warning(message.content)

    response = cl.Message(content='')
    async for chunk in service.chain.astream(message.content):
        await response.stream_token(chunk)
    await response.send()
