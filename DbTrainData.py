import datetime
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from sqlalchemy.sql import func

# https://metanit.com/python/database/3.3.php

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html


class Base(DeclarativeBase):
    pass


class TrainData(Base):
    __tablename__ = "TrainData"
    path = Column(String, primary_key=True)
    result = Column(Integer, nullable=False)
    viewSize = Column(Integer, nullable=False, index=True)
    hasFood = Column(Integer, nullable=False)

class BrainAi(Base):
    __tablename__ = "BrainAi"
    id = Column(Integer,  nullable=False, primary_key=True, autoincrement=True)
    config = Column(String,  nullable=False)
    weigth = Column(String,  nullable=False)
    data = Column(String, nullable=False)
    numTrainings = Column(Integer, nullable=False)
    totalAge = Column(Integer, nullable=False,  default=0)
    eatCount = Column(Integer, nullable=False,  default=0, index=True)
    createdOn = Column(DateTime(), nullable=False, default=func.now())
    updatedOn = Column(DateTime(), nullable=False,
                       default=func.now(),  server_onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(config, weigth),
    )


class DbTrainData():
    # строка подключения
    sqlite_database = "sqlite:///TrainData.db"

    def __init__(self):
        self._engine = create_engine(DbTrainData.sqlite_database, echo=False)
        Base.metadata.create_all(bind=self._engine)

    def __del__(self):
        if self._engine is not None:
            self._engine.dispose()

    def addBulkTrainData(self, pathData):
        with Session(autoflush=False, bind=self._engine) as db:
            # pd = db.query(TrainData).all()

            # a = self.countTable(db, TrainData)
            insertSize = 300
            lsts = [pathData[i:i + insertSize]
                    for i in range(0, len(pathData), insertSize)]

            for l in lsts:
                stmt = sqlite_upsert(TrainData).values(l)
                stmt = stmt.on_conflict_do_nothing(
                    index_elements=[TrainData.path])
                db.execute(stmt)
            db.commit()
            # b=self.countTable(TrainData)
            # print(f"db: all:{b} add:{b-a} input:{len(pathData)}")

    def countTable(self, tableClass: Base) -> int:
        with Session(autoflush=False, bind=self._engine) as db:
            return db.query(tableClass).count()
