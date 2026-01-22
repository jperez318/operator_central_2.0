from enum import Enum
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from db_setup import Base

class TrainingStatus(Enum):
    NOT_TRAINED = 0
    TRAINED = 1
    RAN_IN_WORKSHOP = 2
    SHADOWED = 3
    CAN_TRAIN = 4

class Training_Operator_training_Status(Base):
    __tablename__ = "training_statuses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    training_id = Column(String, ForeignKey("trainings.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    status = Column(String, nullable=False)
    date_assigned = Column(DateTime, nullable=False)