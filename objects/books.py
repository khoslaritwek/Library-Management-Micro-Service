#######################################
# Description of the entity book      #
#######################################         

from pydantic import BaseModel

class Book(BaseModel):
    title           : str
    author          : str
    publishedDate   : str
    pageCount       : int
    isbn            : str
    language        : str
    genere          : str
    isIssued        : bool = False
    issuedDate      : str  = None
    issueeEmail     : str  = None 