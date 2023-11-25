# Library-Management-Micro-Service
Micro Service Codes for Library Management


## Run service by following the steps below:
1. make and activate a virtual environment (always)
2. install requirements.txt
3. open terminal and run uvicorn Service:app


## This is implemented till now
1. User Class and Functionality to create user; users with same user name or email will not be created.
2. Functionality for user to signin into his account. This will be used in services that requires you to authenticate yourself.
3. Endpoint for getting information for a use, but this is restricted to super user admin whose password is obviously is password
4. From this commit onwards seperated user functions from admin functions.
5. Functionality for Super user to add a book added, note all books are trearted as seprate entities, this will be helpful to know which user has accquired which book.
6. User can see all the unique books in the library

## API endpoints
* / -> This is landing page, this will serve as a check if the service is up or not.
* /user/createUser -> API endpoint for User creation.
* /user/signin     -> API endpoint for user to signing to his account.
* /user/listusers  -> This is the endpoint to look all users in the system, this is currently public and all users can userId of other users.
* /admin/getuserinfo/{userId}  -> An admin level functionality that requires Admin level user and access details for a given userId except their passwords.
* /admin/addBook   -> Endpoint for admin level user to add a book to the library.
* /user/listAllBooks -> API Endpoint that list the title and genre of all the unique books available in the library.


### PS: Ill be glad if this code help you!
