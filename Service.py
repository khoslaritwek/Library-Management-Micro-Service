################################################################################
# Author : Ritwek Khosla                                                       #
# Description : Main web app for handling user and assosiated Functionalities  #
################################################################################

# make necessary imports
import warnings 
warnings.filterwarnings('ignore')
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from Dbutils.dataBaseUtils import AddEntery2Db, GetAllUserNames, GetUserinfo, SignIn, AddBook
from objects.user import User
from objects.books import Book
import json

# initiate web app
app = FastAPI()

# landing Fucntion
@app.get("/")
def Root ():
    message = "Welcome to the Library Managment Micoservice: The service is up and running!"
    return {'message' : message, "status" : "success"}

# Function that creates users
@app.post("/user/createUser")
def CreateUser(user : User):

    # Impose a check on  gender
    if user.gender not in ["male", "female", "trans", "others"]:
        return {
            "message" : "Unkown gender, Gender must be in [male, female, trans, others]",
            "status" : "fail"
            }
    
    if user.gender == None:
        user.gender = 'N.A'

    userRespose =  {"user" : user.name, "email" : user.email, "gender" : user.gender}

    # Save Entry to the DB
    saveStatus = AddEntery2Db(user=user)
    if saveStatus != "success":
        return {"message" : saveStatus, "status" : "fail"}

    return {
        "message": "User created successfully",
        "user": userRespose,
        "status" : "success"
        }

# Endpoint for user Signing currently serves as a validator for password only
@app.post("/user/signin")
def UserSigning(userName :str, password: str):
    return SignIn(userName=userName, password=password)

@app.get("/user/listUsers")
def GetUserNameList():
    userList = GetAllUserNames()
    return {"status" : "success", "Users" : userList}

# This is an admin level functionality now
# Admin can see info all other user except their passwords
@app.post("/admin/getuserinfo/{userId}")
def GetUserInfoByName(adminUserName:str, password:str, userId:str):
    # from super users get credentials
    superUserFile = "credentials/superUsers.json"
    with open(superUserFile, "r") as f:
        superUsers = json.load(f)
    
    if adminUserName not in superUsers.keys():
        return {"status" : "fail", "message" : "Unauthorized access"}
    
    # If call was made from a super user verify the password
    signinMessage = SignIn(userName=adminUserName, password=password)
    if signinMessage["status"] != "success":
        return signinMessage

    # now the flow can proceed normally
    status, QueryResults = GetUserinfo(userName=userId)

    if status == "success":
        return {"status" : "sucess", "userdata": QueryResults}
    else:
        return {"status" : "fail", "message" : "User does not exists in the DB"}

# This Function will allow the super user to add a book in the library
@app.post("/admin/addBook")
def AdminAddsBook(adminUserName :str, adminPassword : str, book :Book):
    # from super users get credentials
    superUserFile = "credentials/superUsers.json"
    with open(superUserFile, "r") as f:
        superUsers = json.load(f)
    
    if adminUserName not in superUsers.keys():
        return {"status" : "fail", "message" : "Unauthorized access"}
    
    # If call was made from a super user verify the password
    signinMessage = SignIn(userName=adminUserName, password=adminPassword)
    if signinMessage["status"] != "success":
        return signinMessage
    
    # admin can now Add book
    try:
        mesage = AddBook(book=book)
        return mesage
    except:
        return {"status" : "fail", "message" : "something went wrong, {} book not added".format(book.title)}
