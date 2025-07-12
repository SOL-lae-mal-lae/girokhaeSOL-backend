from pydantic import BaseModel

class ClerkTokenRequest(BaseModel):
    userId:str
