from pydantic import BaseModel

class FunctionCode(BaseModel):
    name: str
    code: str
