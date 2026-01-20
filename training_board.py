from models.operator_obj import Operator
from models.training_obj import Training

class TrainingBoard:
    def __init__(self):
        self.operators = {} #operator_id : Operator object
        self.trainings = {} #training_id : Training object

    def add_operator(self, name):
        new_operator = Operator(name)
        self.operators[new_operator.id] = new_operator
        for training in self.trainings.values():            #assign new operator to all trainings
            training.assign_operator(new_operator.id)

    def delete_operator(self, operator_id_given) -> bool:
        if operator_id_given not in self.operators:
            return False
        del self.operators[operator_id_given]
        for training in self.trainings.values():            #remove operator from all trainings
            training.remove_operator(operator_id_given)
        return True

    def add_training(self, name, amount_of_ops, time_to_train, line, position_in_screen, description):
        new_training = Training(name, amount_of_ops, time_to_train, line, position_in_screen, description)
        for operator_id in self.operators:
            new_training.assign_operator(operator_id)
        self.trainings[new_training.id] = new_training
    
    def delete_training(self, training_id_given) -> bool:
        if training_id_given not in self.trainings:
            return False
        del self.trainings[training_id_given]
        return True

    def toggle_training_priority(self, training_id_given):
        if training_id_given not in self.trainings:
            return False
        self.trainings[training_id_given].priority_flag = not self.trainings[training_id_given].priority_flag

    def get_trainings(self):
        return list(self.trainings.values())
    
    def get_operators(self):
        return list(self.operators.values())
    

