####################################################
# Description: Implementation of the class User    #                              
####################################################

from pydantic import BaseModel
from typing import Optional

# declaring Class for the object User
class User(BaseModel):
    name              : str
    email             : str
    password          : str
    gender            : Optional[str]