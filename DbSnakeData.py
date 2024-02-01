import datetime
from sqlalchemy import Float, create_engine, UniqueConstraint, distinct, inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import insert

# https://metanit.com/python/database/3.3.php

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html


class Base(DeclarativeBase):
    pass


class BrainAi(Base):
    __tablename__ = "BrainAi"
    id = Column(Integer,  nullable=False, primary_key=True, autoincrement=True)
    viewRadius = Column(Integer,  nullable=False, index=True)
    config = Column(String,  nullable=False)
    data = Column(String, nullable=False)
    mse = Column(Float, nullable=False)
    totalAge = Column(Integer, nullable=False, default=0,  server_default="0")
    countEat = Column(Integer, nullable=False, default=0,
                      server_default="0", index=True)
    countStay = Column(Integer, nullable=False,
                       default=0, server_default="0")
    countGiveBirth = Column(Integer, nullable=False,
                            default=0, server_default="0")
    countSurvived = Column(Integer, nullable=False, default=0,
                      server_default="0")

    createdOn = Column(DateTime(), nullable=False,
                       default=datetime.datetime.now,  server_default=func.now())
    updatedOn = Column(DateTime(), nullable=False,
                       default=datetime.datetime.now, server_default=func.now(),  onupdate=datetime.datetime.now, server_onupdate=func.now())
    
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

    '''
    SELECT  100.0*countEat/totalAge, *
    FROM BrainAi
    where totalAge <>0
    order by 1 desc;
            

    SELECT viewSize, COUNT(*)
    FROM TrainData
    GROUP by viewSize        
    '''
  
    def getBestTop(self, countRecords: int = 200) -> list:
        with Session(autoflush=False, bind=self._engine) as db:
            # .where(BrainAi.viewRadius != 2 and BrainAi.mse <= 0.1)
            records = db.query(BrainAi).order_by(
                BrainAi.mse.asc()).limit(countRecords).all()
            return [r.__dict__ for r in records]

    def saveNN(self, info: dict):
        # newNN =  SimpleNN.decode(s)
        with Session(autoflush=False, bind=self._engine) as db:
            columns = [column.name for column in inspect(BrainAi).c]
            # '['id', 'viewRadius', 'config', 'data', 'mse', 'totalAge', 'countEat', 'countStay', 'countGiveBirth', 'createdOn', 'updatedOn']'

            if "id" in info and info["id"] is not None:
                record = db.query(BrainAi).filter(
                    BrainAi.id == info["id"]).first()
            else:
                record = db.query(BrainAi).filter(
                    BrainAi.data == info["data"]).first()

            if record is None:
                b = BrainAi(**info)
                db.add(b)
                db.commit()
            else:
                if "totalAge" in info:
                    record.totalAge += info["totalAge"]
                if "countEat" in info:
                    record.countEat += info["countEat"]
                if "countStay" in info:
                    record.countStay += info["countStay"]
                if "countGiveBirth" in info:
                    record.countGiveBirth += info["countGiveBirth"]
                if "countSurvived" in info:
                    record.countSurvived += info["countSurvived"]
                db.commit()
