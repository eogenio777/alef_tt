from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Town(DeclarativeBase):
    __tablename__ = 'towns'
    town_id = Column(Integer, primary_key=True)
    town_name = Column(String)
    town_district = Column(String)
    town_population = Column(Integer)
    town_wiki_link = Column(String)

    def __repr__(self):
        return "Город: {}\n" \
               "Городской округ: {}\n" \
               "Население (чел.): {}\n" \
               "Ссылка на википедию: {}\n"\
            .format(self.town_name, self.town_district, self.town_population, self.town_wiki_link)
