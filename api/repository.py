from pydantic import BaseModel

from .database import Model

class Repository:
    def __init__(self, model: Model, schema: BaseModel):
        self.model = model
        self.schema = schema

    def get(self, id: int | None) -> BaseModel | None:
        pass
    
    def post(self, model: BaseModel) -> BaseModel:
        pass
    
    def update(self, id: int, model: BaseModel) -> BaseModel | None:
        pass
    
    def delete(self, id: int) -> BaseModel | None:
        pass
