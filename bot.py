import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
from random import randint
import os
import tokens
import json
import pymysql

#BHS Server Log code
token = tokens.token
bhs_server_log = vk_api.VkApi(token=token)
peers = [2000000002]

def log(message):
    for peer in peers:
        bhs_server_log.method('messages.send', {'peer_id': peer, 'message': message, "random_id": randint(-2147483648, 2147483648)})
#Copyright 2019 BHS Studio

def write_msg(peer_id, message):
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, "random_id": randint(-2147483648, 2147483648)})

def send_pic(peer_id, attachment, keyboard, like, dislike):
    vk.method('messages.send', {'peer_id': peer_id, 'message': f'❤ Лайки: {like}\n💔 Дизлайки: {dislike}', 'keyboard': keyboard, 'attachment': attachment, "random_id": randint(-2147483648, 2147483648)})
def isAdmin(user_id):
    admins = os.listdir("./admins/")
    for admin in admins:
        if(str(user_id) == str(os.path.basename(admin))):
            return True
    return False

def get_button(label, color, payload="") :
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload) ,
            "label": label
        },
        "color": color
    }

vk = vk_api.VkApi(
    token=tokens.token #Вставь свой 
)
connected_peers = []
peers = os.listdir("./admins/")
for peer in peers:
    connected_peers.append(int(os.path.basename(peer)))

longpoll = VkBotLongPoll(vk, tokens.groupID, wait = 259200) #Вставь свой ID группы в пустое поле
hello = ["Приветики)", "Hello", "👋🏻", "Привет!", "Здравствуй", "Приветики) Знаешь как пользоваться ботом?) Нет? Тогда напиши /help))"]
otvet = ["Да)?", "Ммм?", "Я знаю, что ты хочешь 😏", "Дай угадать, зачем ты меня зoвешь 😉", "Да?", "Слушаю 😊", "Разработчик бота не несет никакой ответственности за его содержимое!"]

#Load pic count
f = open("./pic", "r")
pic = int(f.read())
f.close()

#Load manga db
f = open("./manga", "r")
manga = []
for line in f.readlines():
    manga.append(line)
f.close()

likeboard = {
    "inline": True, 
    "buttons": [
        [
            get_button(label="Like", color="positive"),    
            get_button(label="Dislike", color="negative"),
            get_button(label="NEED MORE", color="secondary")
        ]
    ]
#тут кнопки добавляются
}

likeboard = json.dumps(likeboard, ensure_ascii=False).encode('utf-8')
likeboard = str(likeboard.decode('utf-8'))

tags = [
    "[CLUB188217821|ХЕНТАЙ]",
    "[CLUB188217821|HENTAI]",
    "[CLUB188217821|@CLUB188217821]",
    "@CLUB188217821"
]

con = pymysql.connect(tokens.serverdb, tokens.userdb, 
    tokens.passworddb, tokens.dbname)

print("STARTED")
#log("✅ Hentai Bot успешно запущен ✅")
for event in longpoll.listen():
    if(event.type == VkBotEventType.MESSAGE_NEW):

        text = event.object.text.upper()
        for tag in tags:
            text = text.replace(tag, '').strip()

        if(text == "ПРИВЕТ" or text == "ХАЙ" or text == "ДАРОВ" or text == "ПРИВ" or text == "ПРИВЕТ ВСЕМ" or text == "ВСЕМ ПРИВЕТ"):
            write_msg(event.object.peer_id, hello[randint(0,len(hello)-1)])
        elif(text=="ХЕНТАЙ"):
            write_msg(event.object.peer_id, otvet[randint(0,len(otvet)-1)])
        elif(text=="/RULES"):
            vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': "✨ Правила беседы ✨\n👉🏻 Нельзя кикать без весомой причины\n👉🏻 Нельзя пиарить\n👉🏻 Нельзя спамить (кроме команд)\n✅ Команды бота: /xxx, /hentai, /хентай\n💬 Помощь: /help\n🗣 Разговорные: Привет, Хентай, Хентай пикчи\n🔞 Предназначено для лиц, старше 18 лет 🔞", "random_id": randint(-2147483648, 2147483648)})
        elif(text=="/HELP"):
            vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': "✨ Команды бота ✨\n🔹 /xxx\n🔹 /hentai\n🔹 /хентай\n🔹 /manga\n👤 Для админов:\n🔹 /admin (id)\n🔹 /unadmin (id)\n🔹 /manga add (url)\n🔹 /manga del (id)\n🔹 /pic (кол-во)\n🔹 /on или /off\n💬 Помощь:\n🔹 /rules\n🔹 /help\n🗣 Разговорные:\n🔹 Привет\n🔹 Хентай\n🔹 Хентай пикчи\n🔞 Ограничение 18 лет 🔞", "random_id": randint(-2147483648, 2147483648)})
        elif(text=="ХЕНТАЙ ПИКЧИ"):
            write_msg(event.object.peer_id, "У меня в коллекции уже " + str(pic) + " картинок 😉")
        elif(text=="/PEER"):
            write_msg(event.object.peer_id, "PeerID этой беседы: " + str(event.object.peer_id))
        elif(event.object.text.split(' ')[0].upper()=="/UNADMIN" and len(event.object.text.split(' ')) == 2):
            if(str(event.object.from_id) == "501702167"):
                try:
                    os.remove("./admins/"+str(event.object.text.split(' ')[1]))
                    write_msg(event.object.peer_id, "Админка отобрана")
                except:
                    write_msg(event.object.peer_id, "Админки у этого человека и не было!")
            else:
                write_msg(event.object.peer_id, "У вас нет на это прав!")
        elif(event.object.text.split(' ')[0].upper()=="/ADMIN" and len(event.object.text.split(' ')) == 2):
            if(str(event.object.from_id) == "501702167"):
                f = open("./admins/"+str(event.object.text.split(' ')[1]), "w")
                f.close()
                write_msg(event.object.peer_id, "Админка выдана")
            else:
                write_msg(event.object.peer_id, "У вас нет на это прав!")
        elif(event.object.text.split(' ')[0].upper()=="/PIC" and len(event.object.text.split(' ')) == 2):
            if(isAdmin(event.object.from_id)):
                try:
                    f = open("./pic", "w")
                    f.write(event.object.text.split(' ')[1])
                    f.close()
                    pic = int(event.object.text.split(' ')[1])
                    write_msg(event.object.peer_id, "Получилось :) Кол-во картинок установлено на " + str(pic))
                except:
                    write_msg(event.object.peer_id, "Не получилось :(")
            else:
                write_msg(event.object.peer_id, "У вас нет на это прав!")
        elif(text=="/ON"):
            if(isAdmin(event.object.from_id)):
                f = open("./peers/"+str(event.object.peer_id), "w")
                f.close()
                connected_peers.append(int(event.object.peer_id))
                write_msg(event.object.peer_id, "Беседа подключена")
            else:
                write_msg(event.object.peer_id, "У вас нет прав на подключение бесед!")
        elif(text=="/OFF"):
            if(isAdmin(event.object.from_id)):
                os.remove("./peers/" + str(event.object.peer_id))
                write_msg(event.object.peer_id, "Беседа отключена")
            else:
                write_msg(event.object.peer_id, "У вас нет прав на подключение бесед!")
        elif(len(event.object.text.split(' ')) == 3 and event.object.text.split(' ')[0].upper()=="/MANGA" and event.object.text.split(' ')[1].upper()=="DEL"):
            if(isAdmin(event.object.from_id)):
                f = open("./peers/"+str(event.object.peer_id), "w")
                f.close()
                manga_id = int(event.object.text.split(' ')[2])
                manga.remove(manga[manga_id])
                f = open("./manga", "w")
                for url in manga:
                    f.write(url+'\n')
                f.close()
                write_msg(event.object.peer_id, "Манга успешно удалена!")
            else:
                write_msg(event.object.peer_id, "У вас нет прав на управление контентом!")
        elif(len(event.object.text.split(' ')) == 3 and event.object.text.split(' ')[0].upper()=="/MANGA" and event.object.text.split(' ')[1].upper()=="ADD"):
            if(isAdmin(event.object.from_id)):
                f = open("./peers/"+str(event.object.peer_id), "w")
                f.close()
                manga.append(event.object.text.split(' ')[2])
                f = open("./manga", "a")
                for url in manga:
                    f.write(url+'\n')
                f.close()
                write_msg(event.object.peer_id, f"Манга успешно добавлена!\n🔑 MangaID: {len(manga)}")
            else:
                write_msg(event.object.peer_id, "У вас нет прав на управление контентом!")
        elif(text=="/MANGA" or text=="/МАНГА"):
            try:
                f = open("./peers/" + str(event.object.peer_id), "r")
                f.close()
                manga_id = randint(0, len(manga)-1)
                write_msg(event.object.peer_id, f"🔞 Случайная хентай манга из базы: {manga[manga_id]}\n🔑 MangaID: {str(manga_id+1)}")
            except Exception as error:
                print(error)
                write_msg(event.object.peer_id, "Эта беседа не подключена! :(")
        elif(text == "NEED MORE" or text=="/XXX" or text=="/ХХХ" or text=="/HENTAI" or text=="/ХЕНТАЙ"):
            try:
                f = open("./peers/" + str(event.object.peer_id), "r")
                f.close()
                while True:
                    #photo-188217821_457239***
                    pic_id = randint(457239022, 457239022 + pic)

                    ###EXCEPT BLOCK###
                    if(pic_id > 457239275 and pic_id < 457239574):
                        continue
                    ###EEXCEPT BLOCK###

                    break
                pic_url = "photo-188217821_" + str(pic_id)
                print(pic_url)

                likeboard = {
                    "inline": True, 
                    "buttons": [
                        [
                            get_button(label=f"Like {pic_id}", color="positive"),    
                            get_button(label=f"Dislike {pic_id}", color="negative"),
                            get_button(label="NEED MORE", color="secondary")
                        ]
                    ]
                #тут кнопки добавляются
                }

                likeboard = json.dumps(likeboard, ensure_ascii=False).encode('utf-8')
                likeboard = str(likeboard.decode('utf-8'))

                con = pymysql.connect(tokens.serverdb, tokens.userdb, 
                    tokens.passworddb, tokens.dbname)
                cur = con.cursor()
                cur.execute("SELECT `likes`, `dislikes` FROM `photos` WHERE id = " + str(pic_id))
                info = cur.fetchall()

                if(len(info) != 0):
                    send_pic(event.object.peer_id, pic_url, likeboard, info[0][0], info[0][1])
                else:
                    send_pic(event.object.peer_id, pic_url, likeboard, 0, 0)

                del likeboard
            except Exception as error:
                print(error)
                write_msg(event.object.peer_id, "Эта беседа не подключена! :(")
        elif(text.split(' ')[0] == 'DISLIKE' and len(text.split(' ')) > 1):
            con = pymysql.connect(tokens.serverdb, tokens.userdb, 
                tokens.passworddb, tokens.dbname)
            cur = con.cursor()
            cur.execute("SELECT `users` FROM `photos` WHERE id = " + text.split(' ')[1])
            info = cur.fetchall()

            if(len(info) != 0):
                liked = False
                for user in info[0][0].split(','):
                    if(user == str(event.object.from_id)):
                        write_msg(event.object.peer_id, f"Вы уже оценили это фото!")
                        liked = True
                if(liked): 
                    continue

                sql = 'UPDATE `photos` SET `likes` = `dislikes` + 1 where id = ' + text.split(' ')[1] + ';'
                cur.execute(sql)
                sql = f"UPDATE `photos` SET `users` = CONCAT(`users`, ',', \"{str(event.object.from_id)}\") where id = {text.split(' ')[1]};"
                cur.execute(sql)
                con.commit()
                con.close()
                write_msg(event.object.peer_id, f"💔 Отметка <<Не нравится>> установлена")
            else:
                sql = f"INSERT INTO `photos` VALUES ({text.split(' ')[1]}, 0, 1, {str(event.object.from_id)});"
                cur.execute(sql)
                con.commit()
                con.close()
                write_msg(event.object.peer_id, f"💔 Отметка <<Не нравится>> установлена")
        elif(text.split(' ')[0] == 'LIKE' and len(text.split(' ')) > 1):
            con = pymysql.connect(tokens.serverdb, tokens.userdb, 
                tokens.passworddb, tokens.dbname)
            cur = con.cursor()
            cur.execute("SELECT `users` FROM `photos` WHERE id = " + text.split(' ')[1])
            info = cur.fetchall()

            if(len(info) != 0):
                liked = False
                for user in info[0][0].split(','):
                    if(user == str(event.object.from_id)):
                        write_msg(event.object.peer_id, f"Вы уже оценили это фото!")
                        liked = True
                if(liked): 
                    continue

                sql = 'UPDATE `photos` SET `likes` = `likes` + 1 where id = ' + text.split(' ')[1] + ';'
                cur.execute(sql)
                sql = f"UPDATE `photos` SET `users` = CONCAT(`users`, ',', \"{str(event.object.from_id)}\") where id = {text.split(' ')[1]};"
                cur.execute(sql)
                con.commit()
                con.close()
                write_msg(event.object.peer_id, f"❤ Отметка <<Нравится>> установлена")
            else:
                sql = f"INSERT INTO `photos` VALUES ({text.split(' ')[1]}, 1, 0, {str(event.object.from_id)});"
                cur.execute(sql)
                con.commit()
                con.close()
                write_msg(event.object.peer_id, f"❤ Отметка <<Нравится>> установлена")
        elif text=='/TEST':
            try:
                write_msg(event.object.peer_id, "Всё работает :)")
            except Exception as e:
                print(e)
