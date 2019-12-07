import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
from random import randint
import os
import tokens

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

def send_pic(peer_id, attachment):
    vk.method('messages.send', {'peer_id': peer_id, 'attachment': attachment, "random_id": randint(-2147483648, 2147483648)})
def isAdmin(user_id):
    admins = os.listdir("./admins/")
    for admin in admins:
        if(str(user_id) == str(os.path.basename(admin))):
            return True
    return False

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
f = open("./pic", "r")
pic = int(f.read())
f.close()
print("STARTED")
log("✅ Hentai Bot успешно запущен ✅")
for event in longpoll.listen():
    if(event.type == VkBotEventType.MESSAGE_NEW):
        if(str(event.object.text).upper() == "ПРИВЕТ" or str(event.object.text).upper() == "ХАЙ" or str(event.object.text).upper() == "ДАРОВ" or str(event.object.text).upper() == "ПРИВ" or str(event.object.text).upper() == "ПРИВЕТ ВСЕМ" or str(event.object.text).upper() == "ВСЕМ ПРИВЕТ"):
            write_msg(event.object.peer_id, hello[randint(0,len(hello)-1)])
        elif(event.object.text.upper()=="ХЕНТАЙ"):
            write_msg(event.object.peer_id, otvet[randint(0,len(otvet)-1)])
        elif(event.object.text.upper()=="/RULES"):
            vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': "✨ Правила беседы ✨\n👉🏻 Нельзя кикать без весомой причины\n👉🏻 Нельзя пиарить\n👉🏻 Нельзя спамить (кроме команд)\n✅ Команды бота: /xxx, /hentai, /хентай\n💬 Помощь: /help\n🗣 Разговорные: Привет, Хентай, Хентай пикчи\n🔞 Предназначено для лиц, старше 18 лет 🔞", "random_id": randint(-2147483648, 2147483648)})
        elif(event.object.text.upper()=="/HELP"):
            vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': "✨ Команды бота ✨\n🔹 /xxx\n🔹 /hentai\n🔹 /хентай\n👤 Для админов:\n🔹 /admin (id)\n🔹 /unadmin (id)\n🔹 /pic (кол-во)\n🔹 /on или /off\n💬 Помощь:\n🔹 /rules\n🔹 /help\n🗣 Разговорные:\n🔹 Привет\n🔹 Хентай\n🔹 Хентай пикчи\n🔞 Ограничение 18 лет 🔞", "random_id": randint(-2147483648, 2147483648)})
        elif(event.object.text.upper()=="ХЕНТАЙ ПИКЧИ"):
            write_msg(event.object.peer_id, "У меня в коллекции уже " + str(pic) + " картинок 😉")
        elif(event.object.text.upper()=="/PEER"):
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
        elif(event.object.text.upper()=="/ON"):
            if(isAdmin(event.object.from_id)):
                f = open("./peers/"+str(event.object.peer_id), "w")
                f.close()
                connected_peers.append(int(event.object.peer_id))
                write_msg(event.object.peer_id, "Беседа подключена")
            else:
                write_msg(event.object.peer_id, "У вас нет прав на подключение бесед!")
        elif(event.object.text.upper()=="/OFF"):
            if(isAdmin(event.object.from_id)):
                os.remove("./peers/" + str(event.object.peer_id))
                write_msg(event.object.peer_id, "Беседа отключена")
            else:
                write_msg(event.object.peer_id, "У вас нет прав на подключение бесед!")
        elif(event.object.text.upper()=="/XXX" or event.object.text.upper()=="/ХХХ" or event.object.text.upper()=="/HENTAI" or event.object.text.upper()=="/ХЕНТАЙ"):
            try:
                f = open("./peers/" + str(event.object.peer_id), "r")
                f.close()
                #photo-188217821_457239***
                pic_id = str(randint(457239022, 457239022 + pic))
                pic_id = "photo-188217821_" + pic_id
                print(pic_id)
                send_pic(event.object.peer_id, pic_id)
            except Exception as error:
                print(error)
                write_msg(event.object.peer_id, "Эта беседа не подключена! :(")
        elif event.object.text.upper()=='/TEST':
            try:
                write_msg(event.object.peer_id, "Всё работает :)")
            except Exception as e:
                print(e)
