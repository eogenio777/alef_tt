from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import DeclarativeBase, Town
from parser import parse_towns_table


class CrudTown:
    def __init__(self, engine_str):
        """
        Инициализация класса взаимодействия с бд
        :param engine_str: стока для подключения к бд
        """
        engine = create_engine(engine_str)
        DeclarativeBase.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        """
        Закоытие всех сессий
        :return:
        """
        self.session.close_all()

    def add_towns(self, towns_list: [[]]):
        """
        Заполнение бд списками городов
        :param towns_list: список с нужными значениями городов
        :return:
        """
        for town_list in towns_list:
            town = Town(
                town_name=town_list[1],
                town_district=town_list[2],
                town_population=town_list[3],
                town_wiki_link=town_list[4]
            )
            self.session.add(town)
            self.session.commit()

    def get_towns(self):
        """
        Строгое получение списка городов из бд
        :return: список городов из бд
        """
        return self.session.query(Town).all()

    def get_town(self, name):
        """
        Получение одного города из бд строго по имени
        :param name: название города
        :return: объект город из бд
        """
        return self.session.query(Town).filter(Town.town_name == name).first()

    def get_towns_alike(self, name):
        """
        Получение одного города из бд нестрого по имени
        :param name: название города
        :return: объект город из бд
        """
        return self.session.query(Town).filter(Town.town_name.ilike(f'%{name}%')).all()

    def delete_extra_from_db_if_needed(self, towns_list: [[]]) -> bool:
        """
        Удаление неактуальных городов из бд
        :param towns_list: список актуальных городов
        :return: флаг изменения - false если изменения не были произведены,
        true - если были
        """
        was_deleted_flag = False
        towns_from_db = self.session.query(Town).all()
        new_names = [item[1] for item in towns_list]
        for town_from_db in towns_from_db:
            if town_from_db.town_name not in new_names:
                print('deleting info')
                self.session.delete(town_from_db)
                self.session.commit()
                was_deleted_flag = True
        return was_deleted_flag

    def add_update_db_if_needed(self, towns_list: [[]]) -> bool:
        """
        Обновление и добавление (если нужно) городов из бд
        :param towns_list: список актуальных городов
        :return: флаг изменения - false если изменения не были произведены,
        true - если были
        """
        was_added_updated_flag = False
        for town_list in towns_list:
            town = Town(
                town_name=town_list[1],
                town_district=town_list[2],
                town_population=town_list[3],
                town_wiki_link=town_list[4]
            )
            town_from_db = self.get_town(town.town_name)
            if town_from_db is None:
                print('adding info')
                self.session.add(town_from_db)
                self.session.commit()
                was_added_updated_flag = True
            elif town.town_population != town_from_db.town_population:
                print('updating info')
                town_from_db.town_population = town.town_population
                self.session.add(town_from_db)
                self.session.commit()
                was_added_updated_flag = True
        return was_added_updated_flag

    def change_db_if_needed(self) -> bool:
        """
        Изменение базы данных по запросу
        :return:  флаг изменения - false если изменения не были произведены,
        true - если были
        """
        was_modified_flag = False
        towns_list = parse_towns_table()
        if len(self.get_towns()) == 0:
            self.add_towns(towns_list)
            was_modified_flag = True
        else:
            del_flag = self.delete_extra_from_db_if_needed(towns_list)
            a_u_flag = self.add_update_db_if_needed(towns_list)
            was_modified_flag = del_flag or a_u_flag
        return was_modified_flag
