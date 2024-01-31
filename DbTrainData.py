import datetime
import json
import numpy as np
from sqlalchemy import create_engine, distinct, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert

from Enums.MoveDirection import MoveDirection


class Base(DeclarativeBase):
    pass


class TrainData(Base):
    __tablename__ = "TrainData"
    path = Column(String, primary_key=True)
    result = Column(Integer, nullable=False)
    viewSize = Column(Integer, nullable=False, index=True)
    hasFood = Column(Integer, nullable=False)


class DbTrainData():
    sqlite_database = "sqlite:///_TrainData.db"

    def __init__(self):
        self._engine = create_engine(DbTrainData.sqlite_database, echo=False)
        Base.metadata.create_all(bind=self._engine)

    def __del__(self):
        if self._engine is not None:
            self._engine.dispose()

    def addBulkTrainData(self, pathData):
        with Session(autoflush=False, bind=self._engine) as db:
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

    def getTrainData(self, viewRadius: int, countRecords: int = 20000) -> tuple:
        with Session(autoflush=False, bind=self._engine) as db:
            records = db.query(TrainData).filter(TrainData.viewSize == viewRadius).order_by(
                func.random()).limit(countRecords).all()
            if len(records)==0:
                return (None, None)

            x = [json.loads(r.path) for r in records]
            x = np.array(x)
            
            y = [([0]*len(MoveDirection), r.result) for r in records]
            y = [(p[0][:p[1]] + [1] + p[0][p[1]+1:], p[1]) for p in y]
            y = np.array([p[0] for p in y])
            return (x, y)

    def getDistinctViewRatius(self)->list:
        with Session(autoflush=False, bind=self._engine) as db:
            records = db.query(distinct(TrainData.viewSize)).all()
            return sorted([r[0] for r in records])