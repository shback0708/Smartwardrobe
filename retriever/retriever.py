# This will be the stub file for retreiver model

# user request, which is going to be the clothes ID
def userRequest(a:int) -> int:

# user-inputted rating of a specific outfit combination
def userFeedback(a:string, b:string) -> None: ...

# updates databse after user removes, takes, returns, adds clothes from/to the rack
def updateDatabase() -> None: ...

# get the angle that the servo needs to rotate
# called by the servo 
def getAngle() -> None: ...


# Here we would have the database setup
# max will be 20 clothes