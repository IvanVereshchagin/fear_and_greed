from app.models.prediction import PredictionHistory
from typing import List, Optional

def get_all_predictions(session) -> List[PredictionHistory]:
    return session.query(PredictionHistory).all()


def get_prediction_by_id(prediction_id: int, session) -> Optional[PredictionHistory]:
    return session.get(PredictionHistory, prediction_id)
    

def get_user_prediction(user_id: str, session) -> Optional[PredictionHistory]:
    prediction = session.query(PredictionHistory).filter(PredictionHistory.user_id == user_id).all()
    if prediction:
        return prediction
    return None

def insert_prediction(new_prediction: PredictionHistory, session) -> None:
    session.add( new_prediction)
    session.commit()
    session.refresh(new_prediction)