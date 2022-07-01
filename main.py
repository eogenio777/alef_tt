from bot import MyBot
import os


def main():
    engine_str = os.environ['DATABASE_URL']
    token = os.environ['TOKEN']
    bot = MyBot(token, engine_str)
    bot.run_bot()


if __name__ == '__main__':
    main()
