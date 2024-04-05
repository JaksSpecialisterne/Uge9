from sqlalchemy import Column, Integer, String, Float, Enum, text
import DatabaseCon

Base = DatabaseCon.Base


LEGAL_MFR = ["A", "G", "K", "N", "P", "Q", "R"]
LEGAL_TYPE = ["C", "H"]
LEGAL_CATEGORIES = {
    "name": [False, str],
    "mfr": [False, str],
    "type": [False, str],
    "calories": [True, int],
    "protein": [True, int],
    "fat": [True, int],
    "sodium": [True, int],
    "fiber": [True, float],
    "carbo": [True, float],
    "sugars": [True, int],
    "potass": [True, int],
    "vitamins": [True, int],
    "shelf": [True, int],
    "weight": [True, float],
    "cups": [True, float],
    "rating": [True, float],
}


class Cereal(Base):

    __tablename__ = "Cereal"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(200))
    mfr = Column(Enum("A", "G", "K", "N", "P", "Q", "R", name="manufacturer"))
    type = Column(Enum("C", "H", name="type"))
    calories = Column(Integer())
    protein = Column(Integer())
    fat = Column(Integer())
    sodium = Column(Integer())
    fiber = Column(Float())
    carbo = Column(Float())
    sugars = Column(Integer())
    potass = Column(Integer())
    vitamins = Column(Integer())
    shelf = Column(Integer())
    weight = Column(Float())
    cups = Column(Float())
    rating = Column(Float())

    def AddToDatabase(self):
        DatabaseCon.session.add(self)
        DatabaseCon.session.commit()

    @staticmethod
    def CerealExists(cerealId: int):
        return (
            DatabaseCon.session.query(Cereal).filter_by(id=cerealId).first() is not None
        )

    @staticmethod
    def GetCerealById(cerealId: int):
        return DatabaseCon.session.get(Cereal, cerealId)

    @staticmethod
    def GetAllCereals():
        return DatabaseCon.session.query(Cereal).all()

    @staticmethod
    def GetCerealByFilters(expressions: list[str]):

        criteria = expressions[0]
        expressions.pop(0)
        for exp in expressions:
            criteria = f"{criteria} AND {exp}"

        sql = text(f"SELECT * FROM uge9.cereal WHERE {criteria}")

        result = DatabaseCon.session.execute(sql)

        resList = []
        for res in result:
            resList.append(res._mapping)

        return resList

    @staticmethod
    def RemoveFromDatabase(cerealId: int):
        DatabaseCon.session.query(Cereal).filter_by(id=cerealId).delete()
        DatabaseCon.session.commit()


def Setup():
    Base.metadata.create_all(DatabaseCon.engine)
