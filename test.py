import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random


class Bot():
    def __init__(self, comleted_id):
        self.comleted_id = comleted_id

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': random.randint(0, 2048)})

    def upload_photo(self, upload, photo):
        response = self.upload.photo_messages(photo)[0]

        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']

        return owner_id, photo_id, access_key

    def send_photo(self, vk, peer_id, owner_id, photo_id, access_key):
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self.vk.method('messages.send', {'user_id': peer_id,
                                         'random_id': random.randint(0, 2048),
                                         'attachment': attachment})

    def finding(self, id):
        profile = self.vk.method('users.get',
                                 {'user_id': id,
                                  'fields': "sex"})
        if id not in list(self.comleted_id.keys()):
            for phrase in self.phares:
                self.write_msg(id, phrase)
            self.write_msg(id,
                           "Готовы узнать, кто вы на самом деле?")
            self.write_msg(id,
                           "Итак, вы.....")
            if profile[0]["sex"] == 1:
                choice = random.choice(list(self.char_female.keys()))
                self.write_msg(id, choice)
                path = self.char_female[choice]
                self.send_photo(self.vk, id, *self.upload_photo(self.upload, path))
                self.comleted_id[id] = [choice, path]
            elif profile[0]["sex"] == 2:
                choice = random.choice(list(self.char_male.keys()))
                self.write_msg(id, choice)
                path = self.char_male[choice]
                self.send_photo(self.vk, id, *self.upload_photo(self.upload, path))
                self.comleted_id[id] = [choice, path]
            else:
                choice = random.choice(list(self.char_common.keys()))
                self.write_msg(id, choice)
                path = self.char_common[choice]
                self.send_photo(self.vk, id, *self.upload_photo(self.upload, path))
                self.comleted_id[id] = [choice, path]
            self.save_files()

        else:
            self.write_msg(id,
                           "Я уже определил, кто вы")
            self.write_msg(id,
                           "Вы")
            self.write_msg(id,
                           self.comleted_id[id][0])
            self.send_photo(self.vk,
                            id,
                            *self.upload_photo(self.upload,
                                               self.comleted_id[id][1]))

    def main(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request_p2 = event.text
                    if event.user_id in list(self.comleted_id.keys()):
                        self.finding(event.user_id)
                    elif (event.user_id not in self.activ_id and
                            event.user_id not in list(self.comleted_id.keys())):
                        self.write_msg(event.user_id,
                                       self.start_phrase)
                        self.activ_id.append(event.user_id)
                        self.save_files()
                    elif (event.user_id in self.activ_id and
                            request_p2.lower() == self.conf_phrase):
                        self.activ_id.remove(event.user_id)
                        self.finding(event.user_id)
                    elif (event.user_id in self.activ_id and
                            request_p2.lower() != self.conf_phrase):
                        self.write_msg(event.user_id,
                                       'Не понял вашего ответа!!!...')



    def save_files(self):
        with open('activ.txt', 'w') as f:
            f.write(str(self.activ_id))
        with open('completed.txt', 'w') as f:
            f.write(str(self.comleted_id))

    def work(self):
        self.main()


    activ_id = []
    token = ""
    vk = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk)
    upload = vk_api.VkUpload(vk)
    char_female = {'Монахиня': "priest_fem.jpg",
                   'Крупье': "dealer_fem.jpg",
                   'Мафиози': "mafia_fem.jpg",
                   'Вышибала': "bouncer_fem.jpg",
                   'Сорвавшая куш': "winner_fem.jpg"}
    char_male = {'Священник': "priest.jpg",
                 'Ночная бабочка': "whore.jpg",
                 'Мафиози': "mafia.jpg",
                 'Банкрот': "bankrupt.jpg",
                 'Сорвавший куш': "winner.jpg"}
    char_common = {'Священник': "priest.jpg",
                   'Ночная бабочка': "whore.jpg",
                   'Монахиня': "priest_fem.jpg",
                   'Крупье': "dealer_fem.jpg",
                   'Мафиози': "mafia.jpg",
                   'Банкрот': "bankrupt.jpg",
                   'Сорвавшая куш': "winner_fem.jpg"}
    phares = ["Определяю личность...",
              "Просматриваю историю браузера...",
              "Заглядываю в сохраненки...",
              "Читаю переписки...",
              "Изучаю гороскоп...",
              "Смотрю на звёзды..."]
    start_phrase = '''Приветствую вас в загадочном
                      распознавателе личности!
                      Сервисе, которой с
                      помощью подлинной магии
                      (или дешёвого фокуса)
                      может с лёгкостью узнать,
                      кем же были именно вы
                      почти 100 лет назад?
                      Если вы готовы отправить
                      в это удивительное приключение,
                      дайте лишь сигнал!
                      Напишите «готов»!'''
    conf_phrase = "готов"