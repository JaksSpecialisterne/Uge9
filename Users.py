from sqlalchemy import Column, Integer, String
import DatabaseCon

Base = DatabaseCon.Base


class User(Base):

    __tablename__ = "User"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(200))
    password = Column(String(200))

    def AddToDatabase(self):
        DatabaseCon.session.add(self)
        DatabaseCon.session.commit()

    @staticmethod
    def UserExist(username: str):
        return (
            DatabaseCon.session.query(User).filter_by(username=username).first()
            is not None
        )

    @staticmethod
    def CorrectPassword(username: str, password: str):
        return (
            DatabaseCon.session.query(User)
            .filter_by(username=username)
            .first()
            .password
            == password
        )

    @staticmethod
    def RemoveFromDatabase(userId: int):
        DatabaseCon.session.query(User).filter_by(id=userId).delete()
        DatabaseCon.session.commit()


def Setup():
    Base.metadata.create_all(DatabaseCon.engine)
