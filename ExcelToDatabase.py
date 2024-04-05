import DatabaseCon
import pandas as pd
from Cereal import Cereal


def FixRating(rating: str) -> float:
    replaced_rating = rating.replace(".", "")
    float_rating = float(replaced_rating)
    return float_rating

def InsertIntoDatabase(filename: str):
    df = pd.read_csv(filename, delimiter=";", skiprows=[1])

    df["rating"] = df.rating.apply(FixRating)

    adf = df.to_dict(orient="records")

    DatabaseCon.session.bulk_insert_mappings(Cereal, adf)
    
    DatabaseCon.session.commit()