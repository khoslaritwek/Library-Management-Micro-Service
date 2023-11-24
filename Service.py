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
from Dbutils.dataBaseUtils import AddEntery2Db, GetAllUserNames, GetUserinfo, SignIn
from objects.user import User

# initiate web app
app = FastAPI()

# landing Fucntion
@app.get("/")
def LandingPage ():
    message = "Welcome to the API landing- it is working"
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
@app.post("/signin")
def UserSigning(userName :str, password: str):
    return SignIn(userName=userName, password=password)


@app.post("/user/{name}")
def GetUserInfoByName(name:str):
    status, QueryResults = GetUserinfo(userName=name)

    if status == "success":
        return {"status" : "sucess", "userdata": QueryResults}
    else:
        return {"status" : "fail", "message" : "User does not exists in the DB"}

@app.get("/user/listUsers")
def GetUserNameList():
    userList = GetAllUserNames()
    return {"status" : "success", "Users" : userList}