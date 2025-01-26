from sqlmodel import Field, SQLModel, create_engine, UniqueConstraint, Relationship
from datetime import datetime
from typing import List, Optional


class tblGenre(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("name", name="genre_constraint"),
    )
    id: int | None = Field(default=None, primary_key=True)
    name: str

class tblBook(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("title", name="title_contstraint"),
    )
    id: int | None = Field(default=None, primary_key=True)
    title: str
    published: datetime
    author: str
    genre_id: int | None = Field(foreign_key="tblgenre.id")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)