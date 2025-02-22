from models.ml_task import MLTask
from typing import List, Optional

def get_all_ml_tasks(session) -> List[MLTask]:
    return session.query(MLTask).all()

def get_ml_task_by_id(task_id: int, session) -> Optional[MLTask]:
    return session.get(MLTask, task_id)
    

def insert_ml_task(new_task: MLTask, session) -> None:
    session.add( new_task )
    session.commit()
    session.refresh(new_task )