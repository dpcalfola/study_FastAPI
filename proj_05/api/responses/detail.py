from pydantic import BaseModel


class DetailResponse(BaseModel):
    """
    DetailResponse represents a response associated with a detailed message
    """
    message: str


class DetailStateCounter(BaseModel):
    message: str
    state: str
    global_state: str
