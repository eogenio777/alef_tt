from bot import MyBot
import os
import re


def main():
    engine_str = os.environ['DATABASE_URL']
    if engine_str.startswith("postgres://"):
        engine_str = engine_str.replace("postgres://", "postgresql://", 1)
    token = os.environ['TOKEN']
    bot = MyBot(token, engine_str)
    bot.run_bot()


if __name__ == '__main__':
    main()
