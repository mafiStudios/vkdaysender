# -*- coding: utf-8 -*-
from datetime import date as dt
from datetime import datetime
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import TOKEN, group_id, chats_id, ver
from defs import answers, log, new_day, sendchat, senduser

vk_session = vk_api.VkApi(token=TOKEN)
longpool = VkBotLongPoll(vk_session, group_id)
VkCheck = True  # Будет ли бот отвечать на сообщения?


def check_events(event):  # Проверка событий
    if event.type == VkBotEventType.MESSAGE_NEW and event.chat_id:  # Если сообщение в чат
        log(f"{event.message['text']} из чата {event.chat_id}", dt.today())
        text = event.message["text"]
        chat_id = event.chat_id
        if "когда" in text:
            new_day(False, event.chat_id, vk_session)
        elif "help" in text or "помощь" in text:
            sendchat(answers("help"), chat_id, vk_session)
        elif "start" in text or "старт" in text or "начать" in text:
            sendchat(answers("start", event), chat_id, vk_session)
        elif "dates" in text or "даты" in text:
            sendchat(answers("watch"), chat_id, vk_session)
        elif "admire" in text or "восхи" in text:
            sendchat(answers("admire"), chat_id, vk_session)
        else:
            sendchat("Не понял", chat_id, vk_session)
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:  # Если сообщение в лс
        log(f"{event.message['text']} от {event.message['from_id']}", dt.today())
        try:
            senduser(text="Бот не отвечает в личных сообщениях.\nДобавьте его в беседу для использования😁",
                     user_id=event.message["from_id"],
                     vk_session=vk_session)
        except Exception:
            pass  # Вылезает ошибка из-за смайлика, но сообщение отправляется. Мое лучшее решение :D


def main():
    olddate, oldtime = "None", "none"
    log(f"daysender {ver} by mafi. \n"
        f"Запуск \n"
        f"Время {datetime.now().time()}", dt.today())
    while True:
        try:
            if VkCheck:
                for event in longpool.check():
                    check_events(event)
        except Exception:
            log("Ошибка vk_api", dt.today())

        time = str(datetime.now().time())
        if time[:5] == "00:00" and str(dt.today()) != olddate:
            log("Новый день!", str(dt.today()))
            new_day(True, chats_id, vk_session)
            olddate = str(dt.today())
        elif time[:4] != oldtime:
            log(f"Время {time}, дата {str(dt.today())}/{olddate}", str(dt.today()))
            oldtime = time[:4]


if __name__ == "__main__":
    main()
