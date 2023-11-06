# -*- coding: utf-8 -*-
import vk_api
from config import TOKEN, group_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token=TOKEN)
lp = VkBotLongPoll(vk_session, group_id)
for event in lp.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.chat_id:
        print(f"chat id = {event.chat_id}")
