from bot import MyBot
import config

# TODO:
#  1) запилить телеграм бота +
#  2) запилить коменты +
#  3) скрыть секреты
#  4) залить на гит
#  5) задеплоить на хероку


def main():
    engine_str = config.engine_str
    token = config.token
    bot = MyBot(token, engine_str)
    bot.run_bot()


if __name__ == '__main__':
    main()
