from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from Cereal import Cereal, LEGAL_MFR, LEGAL_TYPE, LEGAL_CATEGORIES
from Users import User


app = FastAPI()


loggedIn = False


LEGAL_OPERATORS = [
    "<=",
    ">=",
    "!=",
    "<",
    ">",
    "=",
]


@app.get("/", response_class=HTMLResponse)
def ReadRoot():
    return """
    <html>
        <head>
            <title></title>
        </head>
        <body>
            <h1>Welcome to a crunchy experience!</h1>
            <img src="https://th-thumbnailer.cdn-si-edu.com/2zPOHKRmOBMmE66yYYrnGkH_zPE=/1000x750/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/b3/57/b35709d6-a2a4-4abc-933f-aa43cce98513/froot-loops-cereal-bowl.jpg">
        </body>
    </html>
    """


@app.get("/cereals")
def GetCereals():
    return Cereal.GetAllCereals()


@app.get("/cereals/{cerealId}")
def GetCereal(cerealId: int):
    return Cereal.GetCerealById(cerealId)


@app.get(
    "/cereals/filter/{expression}",
    responses={
        406: {"detail": "Category does not exist, error in expression _"},
        406: {
            "detail": "Not a valid operator for this category, error in expression _"
        },
        406: {"detail": "Not a valid operator, error in expression _"},
        406: {
            "detail": "Value given does not match the type of the category queried, error in expression _"
        },
    },
)
def GetCerealsByFilters(expression: str):

    expressions = ExpressionHelper(expression)

    return Cereal.GetCerealByFilters(expressions)


def ExpressionHelper(expression: str) -> list[str]:

    expressions = expression.split("&")
    i = 1
    for exp in expressions:
        tempExp = exp

        # Check if category exists
        for cat in LEGAL_CATEGORIES:
            if cat in tempExp:
                if LEGAL_CATEGORIES[cat] is None:
                    raise HTTPException(
                        status_code=406,
                        detail=f"Category does not exist, error in expression {i}",
                    )
                category = cat
                break

        tempExp = tempExp.replace(category, "")

        # Check if category can use all operators
        for op in LEGAL_OPERATORS:
            if op in tempExp:
                if not (LEGAL_CATEGORIES[category][0]):
                    if operator != "=":
                        raise HTTPException(
                            status_code=406,
                            detail=f"Not a valid operator for this category, error in expression {i}",
                        )
                elif op not in LEGAL_OPERATORS:
                    raise HTTPException(
                        status_code=406,
                        detail=f"Not a valid operator, error in expression {i}",
                    )
                operator = op
                break
        tempExp = tempExp.replace(operator, "")
        value = tempExp

        # checks if the value given is of the same type as the type of the category
        if not (type(value) is LEGAL_CATEGORIES[category][-1]):
            try:
                LEGAL_CATEGORIES[category][-1](value)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=406,
                    detail=f"Value given does not match the type of the category queried, error in expression {i}",
                )
        i += 1

    return expressions


@app.delete(
    "/cereals/{cerealId}",
    responses={
        406: {"detail": "Cereal does not exist and thus cannot be deleted"},
        401: {"detail": "Not logged in, log in to try again"},
    },
)
def DeleteCereal(cerealId: int):
    MustBeLoggedIn()
    if not Cereal.CerealExists(cerealId):
        raise HTTPException(
            status_code=406,
            detail="Cereal does not exist and thus cannot be deleted",
        )
    Cereal.RemoveFromDatabase(cerealId)
    return {"ok": True}


@app.post("/login")
def Login(username, password):
    if User.UserExist(username) and User.CorrectPassword(username, password):
        global loggedIn
        loggedIn = True


@app.post("/register")
def Register(username, password):
    if not User.UserExist(username):
        user = User(username, password)
        user.AddToDatabase()


@app.post("/logout")
def Logout():
    global loggedIn
    loggedIn = False


def MustBeLoggedIn():
    if not loggedIn:
        raise HTTPException(
            status_code=401,
            detail="Not logged in, log in to try again",
        )


@app.post(
    "/cereals/{cerealId}",
    responses={
        406: {
            "detail": "Cereal does not exist, you cannot determine ID yourself when creating new cereal"
        },
        401: {"detail": "Not logged in, log in to try again"},
    },
)
def PostCerealUpdate(cerealId):
    MustBeLoggedIn()
    if not Cereal.CerealExists(cerealId):
        raise HTTPException(
            status_code=406,
            detail="Cereal does not exist, you cannot determine ID yourself when creating new cereal",
        )


@app.post(
    "/cereals",
    responses={
        406: {"detail": "Manufacturer given not legal"},
        406: {"detail": "Temperature type given not legal"},
        401: {"detail": "Not logged in, log in to try again"},
    },
)
def PostCerealNew(
    name: str,
    mfr: str,
    type: str,
    calories: int,
    protein: int,
    fat: int,
    sodium: int,
    fiber: float,
    carbo: float,
    sugars: int,
    potass: int,
    vitamins: int,
    shelf: int,
    weight: float,
    cups: float,
    rating: float,
):
    MustBeLoggedIn()
    if mfr not in LEGAL_MFR:
        raise HTTPException(status_code=406, detail="Manufacturer given not legal")

    if type not in LEGAL_TYPE:
        raise HTTPException(status_code=406, detail="Temperature type given not legal")

    cereal = Cereal(
        name=name,
        mfr=mfr,
        type=type,
        calories=calories,
        protein=protein,
        fat=fat,
        sodium=sodium,
        fiber=fiber,
        carbo=carbo,
        sugars=sugars,
        potass=potass,
        vitamins=vitamins,
        shelf=shelf,
        weight=weight,
        cups=cups,
        rating=rating,
    )
    cereal.AddToDatabase()
