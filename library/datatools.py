from model import tblBook, engine
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

def add_book(en: Engine, title: str, genre:str, author: str, published: str) -> bool:
    date_object = datetime.strptime(published, r"%d.%m.%Y")
    with Session(en) as session:
        book = tblBook(
            title=title, 
            genre=genre, 
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

def get_all_data(en: Engine) -> list:
    with Session(en) as session:
        query = select(tblBook)
        return [
            (x.title, x.author, x.genre, x.published) 
            for x in session.exec(query).all()]


if __name__ == "__main__":
    ...