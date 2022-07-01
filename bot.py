from telebot import TeleBot
from crud import CrudTown


class MyBot:
    def __init__(self, token, engine_str):
        self.bot = TeleBot(token)
        self.crud = CrudTown(engine_str)

    def run_bot(self):
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, "Это тестовое задание для комании Alef Development.\n"
                                                   "Для начала работы введите команду /update - она "
                                                   "обновит базу данных. \n"
                                                   "Для поиска городов введите название города или его часть!\n"
                                                   "Для получения справки и ссылок введите команду /help")

        @self.bot.message_handler(commands=['help'])
        def help_message(message):
            self.bot.send_message(message.chat.id, '/update - обновляет бд\n'
                                                   '/start - вывод приветствия\n'
                                                   'Пользовательский ввод воспринимается как название '
                                                   'или часть названия города.\n\n'
                                                   'Контакты (Подружиснкий Евгений Дмитриевич):\n'
                                                   '-tg: @estop10\n'
                                                   '-почта: evg.pod.dm@gmail.com\n'
                                                   '-hh-резюме: https://spb.hh.ru/resume/ab764334ff0afe87de0039ed1f476855574d54 \n'
                                                   '-github (с кодом данного проекта): https://github.com/eogenio777')

        @self.bot.message_handler(commands=['update'])
        def update_db(message):
            flag_changed = self.crud.change_db_if_needed()
            if flag_changed:
                self.bot.send_message(message.chat.id, 'База данных была обновлена!')
            else:
                self.bot.send_message(message.chat.id, 'База данных не была обновлена, данные актуальны!')

        @self.bot.message_handler(func=lambda message: True)
        def find_town(message):
            towns = self.crud.get_towns_alike(message.text)
            if len(towns) == 0:
                self.bot.send_message(message.chat.id, f'Не существует городов, в названиях которых присутствует:'
                                                       f' \'{message.text}\'')
            else:
                for town in towns:
                    self.bot.send_message(message.chat.id, town)

        self.bot.infinity_polling()
