from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert

# https://metanit.com/python/database/3.3.php

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html


class Base(DeclarativeBase):
    pass


class PathDataInfo(Base):
    __tablename__ = "PathDataInfo"
    path = Column(String, primary_key=True, index=True)
    result = Column(Integer, nullable=False)
    viewSize = Column(Integer, nullable=False)
    hasFood = Column(Integer, nullable=False)


class DbPathData():
    # строка подключения
    sqlite_database = "sqlite:///PathData.db"

    def __init__(self):
        self._engine = create_engine(DbPathData.sqlite_database, echo=False)
        Base.metadata.create_all(bind=self._engine)

    def __del__(self):
        if self._engine is not None:
            self._engine.dispose()

    def addBulk(self, pathData):
        with Session(autoflush=False, bind=self._engine) as db:
            # pd = db.query(PathDataInfo).all()

            # a = self.countTable(db, PathDataInfo)
            insertSize = 300
            lsts = [pathData[i:i + insertSize]
                    for i in range(0, len(pathData), insertSize)]

            for l in lsts:
                stmt = sqlite_upsert(PathDataInfo).values(l)
                stmt = stmt.on_conflict_do_nothing(
                    index_elements=[PathDataInfo.path])
                db.execute(stmt)
            db.commit()
            # b=self.countTable(PathDataInfo)
            # print(f"db: all:{b} add:{b-a} input:{len(pathData)}")
        
    def countTable(self, tableClass: Base)->int:
        with Session(autoflush=False, bind=self._engine) as db:        
            return db.query(tableClass).count()
