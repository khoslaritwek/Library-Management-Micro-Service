###################################################################################
# Author: Ritwek Khosla                                                           #
# Description : Script for Creating user DB                                       #
###################################################################################

# make necessary import 
import warnings
warnings.filterwarnings("ignore")
import sqlite3
from pydantic import BaseModel
from typing import Optional
from objects.user import User


# A Function for creating Users db, in case a db exists recalling this
# Function will create a new db, new fileds can be added here

def CreateDb(dbPath :str = 'mydatabase.db'):
   conn = sqlite3.connect(dbPath) 
   cursor = conn.cursor()
   cursor.execute(
    '''CREATE TABLE IF NOT EXISTS allUsers (
    name TEXT PRIMARY KEY,
    email TEXT,
    password TEXT,
    gender TEXT);
                  ''')

   conn.commit()
   conn.close()


def AddEntery2Db(dbPath :str = 'mydatabase.db', user : User = None):
   conn = sqlite3.connect(dbPath)
   cursor = conn.cursor() 

   # lets First check if user exists or not
   cursor.execute("SELECT COUNT(*) FROM allUsers WHERE name=?", (user.name,))
   nameCount = cursor.fetchone()
   
   # imposing a check on email-id as well
   cursor.execute("SELECT COUNT(*) FROM allUsers WHERE email=?", (user.email,))
   EmailCount = cursor.fetchone()
   
   # no need to add If user Already Exists in DB
   if nameCount[0] != 0:
      print('[info]: User name already exists')
      conn.close
      return "User name already Exists in DB"
   
   if EmailCount[0] != 0:
      print('[info]: Email Id Exists in DB already')
      conn.close()
      return "Supplied Email-Id alreadyy Exists"


   row2Insert = [(user.name, user.email, user.password, user.gender)]
   cursor.executemany("INSERT INTO allUsers (name, email, password, gender) VALUES (?, ?, ?, ?)", row2Insert)
   conn.commit()
   conn.close()

   return "success"


# Function for getting user names in the DB
def GetAllUserNames(dbPath :str = 'mydatabase.db'):
   conn = sqlite3.connect(dbPath)
   cursor = conn.cursor()

   cursor.execute("SELECT name FROM allUsers") 
   results = cursor.fetchall()
   user_names = [result[0] for result in results]

   return user_names

# Function for retriving information of a user from DB
def GetUserinfo (userName:str, dbPath :str = 'mydatabase.db'):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, email, gender FROM allUsers WHERE name=?", (userName,))
    result = cursor.fetchone()
    conn.close()

    if result:
       return ("success", {"name" : result[0], "email" : result[1], "gender" : result[2]})
    else:
       return ("fail", "")
    
# Implementation of Signin Functionality
def SignIn(userName:str, password:str, dbPath = "mydatabase.db"):
   # make query to the DB for username
   conn = sqlite3.connect('mydatabase.db')
   cursor = conn.cursor()
   cursor.execute("SELECT name, password FROM allUsers WHERE name=?", (userName,))
   result = cursor.fetchone()
   conn.close()

   if not result:
      return {"status" : "fail", "message" : "user does not exit in db"}
   elif result and (result[1] != password):
      return {"status" : "fail", "message" : "wrong password"}
   elif result and (result[1] == password):
    return {"status" : "success", "message" : "login successful"}

if __name__ == "__main__":
   CreateDb()

   # Define a Pydantic object
   user = User(name='RitwekMahan-123', email="ritwekMan@gmail.com", password = '123456', gender= "male")

   # Insert into db
   AddEntery2Db(user=user)

   # Get all user list
   print(GetAllUserNames())

   # get info about one user
   print(GetUserinfo(userName='Ritwek'))