from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

class Database:
    __instance = None

    def  __init__(self, username, password):
        if Database.__instance is None:
            Database.__instance = Database.__impl(username, password)
    
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)
    
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)  
    
    class __impl:
        def __init__(self, username, password):
            self.engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@localhost/uge9")
            self.Base = declarative_base()
            self.metadata = MetaData()


