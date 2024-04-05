# Requirements
Requires you to create a database in MySQL called uge9, this can done from the MySQL command line using "CREATE DATABASE uge9"

Also requires you to have a user called uge9. This can also be made from the mysql line using "CREATE USER 'uge9'@'localhost' IDENTIFIED BY 'uge9';"
Then you should give it privileges by GRANT ALL PRIVILEGES ON * . * TO 'uge9'@'localhost';
All given priveleges are not needed and in reality it should only give those required, but for this case this is the easiest.


# How to use:
The program to run is "Main.py", you can give Main.py an additionaly argument, which is the name of a csv file you wish to insert into the database so first time users should use the Cereal.csv file and do "Main.py Cereal.csv"

After it is opened you can go to http://127.0.0.1:8000/docs/ and try it out, or go to http://127.0.0.1:8000 to watch the glorious welcome site

You must be logged in to do anything beside using the GET, it should be noted that passwords and usernames are not in anyway secure and are stored as plaintext in the database (WHICH IS A VERY BAD IDEA), but this is just to fufill requirements and more time and energy would be needed to properly secure it

# Observationer:
Der er stadig ting som kunne være mere effiktive eller bedre implementeret, såsom filtrering kunne nok godt være mere yndigt.
Billeder bliver heller ikke vist for de forskellige cereals, detter ville bare være et spørgsmål om at gemme en reference til et lokalt url eller et url til en website som har et billede, dette ville så kunne enten sende videre eller vises som billedet på forsiden vises.
