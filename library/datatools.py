from model import tblBook, engine, tblGenre
from sqlmodel import Session, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, IntegrityError
from datetime import datetime

from loguru import logger


logger.add("error.log", level="INFO", format="{time} {level} {message}")

def check_title_exists(en: Engine, title: str) -> bool:
    with Session(en) as session:
        result = select(tblBook).where(tblBook.title == title)
        if session.exec(result).first():
            return True
        else: 
            return False

def check_genre_exists(en: Engine, name: str) -> bool:
    with Session(en) as session:
        result = select(tblGenre).where(tblGenre == name)
        if session.exec(result).first():
            return True
        else: 
            return False

def add_genre(en: Engine, name: str) -> bool:
    with Session(en) as session:
        query = tblGenre(name=name)
        session.add(query)
        try:
            session.commit()
            return check_genre_exists(en, name)
        except IntegrityError as e:
            logger.error(f"[!] {e}")
            return False
        except Exception as e:
            logger.error(f"[!] Das Genre konnte nicht hinzugefügt werden {e}")
            return False


def add_book(en: Engine, title: str, genre:str, author: str, published: str) -> bool:
    date_object = datetime.strptime(published, r"%d.%m.%Y")
    with Session(en) as session:
        # Hole das angegebene Genre. Achtung, es muss existieren!
        query = select(tblGenre).where(tblGenre.name == genre)
        genre_obj = session.exec(query).first()
        
        book = tblBook(
            title=title, 
            genre_id=genre_obj.id, 
            author=author, 
            published=date_object)
        
        session.add(book)

        try:
            session.commit()
            # Prüft ob das Hinzufügen geklappt hat
            return check_title_exists(en, title)           
        except IntegrityError as e:
            logger.error(f"[!] {e}")
            return False
        except Exception as e:
            logger.error(f"Das Buch konnte nicht eingefügt werden! {e}")
            return False

def remove_book(en: Engine, title: str):
    with Session(en) as session:
        book = select(tblBook).where(tblBook.title == title)
        result = session.exec(book)
        try: 
            session.delete(result.one())
            session.commit()
            if not session.exec(book).first():
                return True
            else:
                return False
        except MultipleResultsFound: 
            logger.error("Unter diesem Title wurden mehrere Bücher gefunden!")
            return False
        except NoResultFound as e:
            logger.error("Unter dem Title konnte nichts gefunden werden!")
            return False
        
def get_all_category(en: Engine) -> list:
    with Session(en) as session:
        query = select(tblGenre.name)
        return [genre for genre in session.exec(query).all()]

def get_all_data(en: Engine) -> list:
    with Session(en) as session:
        query = select(tblBook)
        return [
            (x.title, x.author, x.genre, x.published) 
            for x in session.exec(query).all()]


if __name__ == "__main__":
    ...