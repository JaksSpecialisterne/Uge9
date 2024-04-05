from Database import Database
from sqlalchemy.orm import Session

database = Database("uge9","uge9")
engine = database.engine
Base = database.Base
Base.metadata.create_all(bind=engine)
session = Session(engine, autoflush=False)