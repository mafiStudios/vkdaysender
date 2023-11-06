# -*- coding: utf-8 -*-
from datetime import date as dt
from datetime import datetime
from config import ver, dates


def sendchat(text, ids, vk_session):
    if type(ids) == list:
        for id1 in ids:
            vk_session.method("messages.send", {"chat_id": id1, "message": text, "random_id": 0})
    elif type(ids) == int:
        vk_session.method("messages.send", {"chat_id": ids, "message": text, "random_id": 0})


def senduser(text, user_id, vk_session):
    vk_session.method("messages.send", {"user_id": user_id, "message": text, "random_id": 0})


def answers(ans, event=0):
    match ans:
        case "start":
            time, date = str(datetime.now().time())[:8], str(dt.today())
            start = f"""bot daysender v{ver}.\nВремя:{time[:8]}⏰\nДата:{date}📆 \nАйди чата:{event.chat_id}"""
            return start
        case "help":
            help_message = f"""Команды:
*Вызываются в сообщении после упоминания бота (@bot команда)\nstart/старт/начать - вызов статового меню🐵
help/помощь - вызов команд😶\ndates/даты - показать даты📜\nadmire/восхищаться - Восхититься создателем
                """
            return help_message
        case "watch":
            t = ""
            for i in dates:
                t += f'"{i}" - {dates[i]}\n'
            return t
        case "admire":
            return "Вы восхитились🎉"


def declination(value):
    words = ['день', 'дня', 'дней']
    try:
        if all((value % 10 == 1, value % 100 != 11)):
            return words[0]
        elif all((2 <= value % 10 <= 4, any((value % 100 < 10, value % 100 >= 20)))):
            return words[1]
        return words[2]
    except:
        return "дня"  # Если нет даты(Unknown например)


def monthdecl(value):
    months = {"January": "январе", "February": "феврале", "March": "марте", "April": "апреле", "May": "мае",
              "June": "июне", "July": "июле", "August": "августе", "September": "сентябре", "October": "октябре",
              "November": "ноябре", "December": "декабре"}
    return months[value]


def int0(numb):
    if numb[0] == "0":
        return int(numb[1:])
    else:
        return int(numb)


def log(text, datenow):
    print(text)
    with open(f"logs{datenow}.txt", "a") as file:
        file.write("\n" + str(text))
        file.close()


def sort_days(num):
    num = num[1]
    if len(num.split("|")) > 1:
        return int0(num.split("|")[0])
    elif num == "unknown":
        return 99999
    else:
        return int0(num)


def get_days():
    now, full = dt.today(), []
    for name in dates:
        ldate = dates[name].split("-")
        if len(ldate) < 2:
            full.append([name, str(dates[name]), dates[name], "non"])
        elif ldate[2] == "00":
            todate = dt(int0(ldate[0]), int0(ldate[1]), int0(ldate[2]) + 1)
            full.append([name, f"{str((todate - now).days)}|{str(dt.today().strftime('%B'))}", dates[name], "month"])
        else:
            todate = dt(int0(ldate[0]), int0(ldate[1]), int0(ldate[2]))
            full.append([name, str((todate - now).days), dates[name], "day"])
    return sorted(full, key=sort_days)


def new_day(new, ids, vk_session):
    datelist, message = get_days(), ""
    for i in range(0, len(dates)):
        match datelist[i][3]:
            case "day":
                if int0(datelist[i][1].split("|")[0]) > 0:
                    message += f"До '{datelist[i][0]}' осталось {datelist[i][1]} {declination(int(datelist[i][1]))}\n"
                elif int0(datelist[i][1].split("|")[0]) == 0:
                    message += f"{datelist[i][0]} сегодня\n"
                else:
                    message += f"{datelist[i][0]} было\n"
            case "month":
                l1 = datelist[i][1].split("|")
                if int(l1[0]) > 0:
                    message += f"'{datelist[i][0]}' будет в {monthdecl(l1[1])}, " \
                               f"то есть через {l1[0]} {declination(int(l1[0]))}\n"
                elif int(l1[0]) < -30:
                    message += f"'{datelist[i][0]}' будет в {monthdecl(l1[1])}\n"
                else:
                    message += f"{datelist[i][0]} было\n"
            case "non":
                message += f"До '{datelist[i][0]}' осталось {datelist[i][1]}\n"
    if new:
        sendchat("Новый день.", ids, vk_session)
    sendchat(message, ids, vk_session)
