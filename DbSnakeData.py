import datetime
from sqlalchemy import Float, create_engine, UniqueConstraint
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
    data = Column(String, nullable=False)
    mse = Column(Float, nullable=False)
    totalAge = Column(Integer, nullable=False,  server_default="0")
    countSteps = Column(Integer, nullable=False,
                        server_default="0", index=True)
    countEat = Column(Integer, nullable=False,  server_default="0", index=True)
    countStay = Column(Integer, nullable=False,  server_default="0")
    countGiveBirth = Column(Integer, nullable=False,  server_default="0")
    createdOn = Column(DateTime(), nullable=False, server_default=func.now())
    updatedOn = Column(DateTime(), nullable=False,
                       server_default=func.now(),  server_onupdate=func.now())
    __table_args__ = (
        UniqueConstraint(data),
    )

# select.order_by(func.random())


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

    def saveNN(self, info: dict, mse: float):
        with Session(autoflush=False, bind=self._engine) as db:
            record = db.query(BrainAi).filter(
                BrainAi.data == info["data"]).first()
            if record is None:
                db.add(BrainAi(config=info["config"],
                       data=info["data"], mse=round(mse,4)))
                db.commit()
            else:
                pass
