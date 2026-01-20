import uuid
from models.training_statuses import TrainingStatus

class Training:
    def __init__(self, name, amount_of_ops, time_to_train, line, position_in_screen, description, id=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.amount_of_ops = amount_of_ops
        self.time_to_train = time_to_train
        self.line = line
        self.priority_flag = True
        self.position_in_screen = position_in_screen
        self.description = description
        self.operator_statuses = {}

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