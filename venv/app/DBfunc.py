import mysql
import mysql.connector
from app import routes
from app import leaguecalls
import hashlib

LOLDB = mysql.connector.connect(        #connect database
    host="localhost",
    user="root",
    password="",
    database="stattracker"
)

dbcursor = LOLDB.cursor()               #easier database coll-age
dbcursor = LOLDB.cursor(buffered=True)



##I'm not making this object oriented as there is no need for it to be


def verifyLogin(givenUser,Password):  #verifies login for main page
    dbcursor.execute(f'SELECT UserPassword FROM stattracker.User WHERE Username = "{givenUser}"; ')
    hashedPassword = hashlib.sha1(Password.encode()).hexdigest()
    Login = dbcursor.fetchone()
    if Login[0].lower() == hashedPassword.lower():
        return True
    else:
        return False



def loadUsername(givenUser): #loads LEAGUE OF LEGENDS username for other functions
    dbcursor.execute(f'SELECT LeagueUser FROM stattracker.User WHERE Username = "{givenUser}"; ')
    LeagueUser = dbcursor.fetchone()
    return LeagueUser[0]

def createUser(Username, Password, LeagueUsername):  #creates uername for dataebase
    leagueusername = leaguecalls.summonerInfo(LeagueUsername)
    currentGamer = leaguecalls.requestSummoner(leagueusername)
    currentGamer.requestfunc()
    currentGamer.parseResponse()
    name = currentGamer.getChosenSummoner().getSummonerName()
    hashedPassword = hashlib.sha1(Password.encode()).hexdigest()
    dbcursor.execute(f'INSERT INTO stattracker.User (Username, UserPassword, LeagueUser) VALUES (%s, %s, %s) ',(Username, hashedPassword, name))
    LOLDB.commit()
    #print(f"User {Username} created.")

