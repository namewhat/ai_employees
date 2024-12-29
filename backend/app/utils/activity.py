from sqlalchemy.orm import Session
from app.models.base import Activity

def record_activity(db: Session, type: str, content: str):
    """记录一个活动"""
    activity = Activity(type=type, content=content)
    db.add(activity)
    db.commit()
    return activity 