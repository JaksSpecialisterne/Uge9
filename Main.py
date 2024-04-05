import sys, os, Users
import DatabaseSetup, ExcelToDatabase


if __name__ == "__main__":
    DatabaseSetup.Setup()

    if not Users.User.UserExist("admin"):
        user = Users.User(username="admin", password="admin")
        user.AddToDatabase()

    arg = ""
    if not sys.argv:
        arg = sys.argv.pop()

    if arg != "":
        ExcelToDatabase.InsertIntoDatabase(arg)
    os.system("uvicorn API:app --reload")
