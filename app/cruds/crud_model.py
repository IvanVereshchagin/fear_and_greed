from models.model import Model
from typing import List, Optional

def get_all_models(session) -> List[Model]:
    return session.query(Model).all()

def get_model_by_id(model_id: int, session) -> Optional[Model]:
    return session.get(Model, model_id)
    

def insert_model(new_model: Model, session) -> None:
    session.add( new_model )
    session.commit()
    session.refresh(new_model)