import datetime
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

# https://metanit.com/python/database/3.3.php

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html


class Base(DeclarativeBase):
    pass


class BrainAi(Base):
    __tablename__ = "BrainAi"
    id = Column(Integer,  nullable=False, primary_key=True, autoincrement=True)
    config = Column(String,  nullable=False, index=True)
    weigth = Column(String,  nullable=False, index=True)
    bias = Column(String,  nullable=False, index=True)
    data = Column(String, nullable=False)
    numTrainings = Column(Integer, nullable=False)
    totalAge = Column(Integer, nullable=False,  server_default="0")
    eatCount = Column(Integer, nullable=False,  server_default="0", index=True)
    countGiveBirth = Column(Integer, nullable=False,  server_default="0")
    createdOn = Column(DateTime(), nullable=False, server_default=func.now())
    updatedOn = Column(DateTime(), nullable=False,
                       server_default=func.now(),  server_onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(config, weigth, bias),
    )


class DbSnakeData():
    sqlite_database = "sqlite:///_SnakeData.db"

    def __init__(self):
        self._engine = create_engine(DbSnakeData.sqlite_database, echo=False)
        Base.metadata.create_all(bind=self._engine)

    def __del__(self):
        if self._engine is not None:
            self._engine.dispose()

    def countTable(self, tableClass: Base) -> int:
        with Session(autoflush=False, bind=self._engine) as db:
            return db.query(tableClass).count()
