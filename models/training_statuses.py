from enum import Enum
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from db_setup import Base

class TrainingStatus(Enum):
    NOT_TRAINED = "not_trained"
    TRAINED = "trained"
    RAN_IN_WORKSHOP = "ran_in_workshop"
    SHADOWED = "shadowed"
    CAN_TRAIN = "can_train"

class Training_Operator_training_Status(Base):
    __tablename__ = "training_statuses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    training_id = Column(String, ForeignKey("trainings.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    status = Column(String, nullable=False)
    date_assigned = Column(DateTime, nullable=False)