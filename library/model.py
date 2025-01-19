from sqlmodel import Field, SQLModel, create_engine, UniqueConstraint
from datetime import datetime


class tblBook(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("title", name="title_contstraint"),
    )
    id: int | None = Field(default=None, primary_key=True)
    title: str
    genre: str
    published: datetime
    author: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)