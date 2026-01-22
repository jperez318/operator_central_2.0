from sqlalchemy import Column, Integer, String, Boolean
from db_setup import Base
import uuid
from models.training_statuses import TrainingStatus

class Training(Base):
    __tablename__ = "trainings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    amount_of_ops_needed = Column(String, nullable=False)
    time_to_train = Column(String, nullable=False)
    line = Column(String, nullable=False)
    priority_flag = Column(Boolean, default=False)
    position_in_screen = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operator_statuses = {} # This will not be a column in the DB; it's managed in application logic
    
    def assign_operator(self, operator_id: str):
        self.operator_statuses[operator_id] = TrainingStatus.NOT_TRAINED

    def remove_operator(self, operator_id) -> bool:
        if operator_id not in self.operator_statuses:
            return False # Should never happen since operators should either be assigned to every training or not assigned at all
        del self.operator_statuses[operator_id]
        return True

    def reset_operator_statuses(self):
        for operator_id in self.operator_statuses:
            self.operator_statuses[operator_id] = TrainingStatus.NOT_TRAINED

    def to_String(self):
        return f"<Training(id={self.id}, name={self.name}, amount_of_ops={self.amount_of_ops_needed}, time_to_train={self.time_to_train}, line={self.line}, priority_flag={self.priority_flag}, position_in_screen={self.position_in_screen}, description={self.description})>"