from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
  
# https://metanit.com/python/database/3.3.php

class Base(DeclarativeBase): pass
class PathDataInfo(Base):
    __tablename__ = "PathDataInfo"
    path = Column(String, primary_key=True, index=True)
    result = Column(Integer, nullable = False)
    viewSize = Column(Integer, nullable = False)

class DbOperations():
    # строка подключения
    sqlite_database = "sqlite:///PathData.db"

    def __init__(self):    
        self._engine = create_engine(DbOperations.sqlite_database, echo=False)
        Base.metadata.create_all(bind=self._engine)
 

    def addBulk(self, pathData):
        with Session(autoflush=False, bind=self._engine) as db:
            # pd = db.query(PathDataInfo).all()

            stmt = sqlite_upsert(PathDataInfo).values(pathData)
# ...     [
# ...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
# ...         {"name": "sandy", "fullname": "Sandy Cheeks"},
# ...         {"name": "patrick", "fullname": "Patrick Star"},
# ...         {"name": "squidward", "fullname": "Squidward Tentacles"},
# ...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
# ...     ]
            stmt = stmt.on_conflict_do_nothing(index_elements=[PathDataInfo.path])
            db.execute(stmt)
            db.commit()

    def getCountRows(self)            :
        with Session(autoflush=False, bind=self._engine) as db:
            return db.query(PathDataInfo).count()