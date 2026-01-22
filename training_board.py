from collections import defaultdict
from datetime import datetime
from db_setup import SessionLocal
from models.operator_obj import Operator
from models.training_obj import Training
from models.training_statuses import Training_Operator_training_Status, TrainingStatus

class TrainingBoard:
    def __init__(self):
        self.operators = {}  # operator_id: Operator object
        self.trainings = {}  # training_id: Training object
        self.load_from_db()

    def load_from_db(self):
        db = SessionLocal()

        # Loads operators
        for op in db.query(Operator).all():
            self.operators[op.id] = op

        # Loads trainings
        trainings = db.query(Training).all()
        operators_ids = list(self.operators.keys())

        # Loads training statuses
        status_rows = db.query(Training_Operator_training_Status).all()
        training_dict = defaultdict(dict)
        for row in status_rows:
            training_dict[row.training_id][row.operator_id] = row.status

        # Populate each training's operator_statuses
        for training in trainings:
            training.operator_statuses = {op_id: TrainingStatus.NOT_TRAINED for op_id in operators_ids}
            if training.id in training_dict:
                training.operator_statuses.update(training_dict[training.id])
            self.trainings[training.id] = training

        db.close()

    def add_operator(self, name):
        db = SessionLocal()
        new_operator = Operator(name)
        db.add(new_operator)
        db.commit()
        db.close()

        self.operators[new_operator.id] = new_operator
        for training in self.trainings.values():
            training.assign_operator(new_operator.id)

    def delete_operator(self, operator_id):
        if operator_id not in self.operators:
            return False
        db = SessionLocal()
        db.query(Operator).filter_by(id=operator_id).delete()
        db.query(Training_Operator_training_Status).filter_by(operator_id=operator_id).delete()
        db.commit()
        db.close()

        del self.operators[operator_id]
        for training in self.trainings.values():
            training.remove_operator(operator_id)
        return True

    def add_training(self, name, amount_of_ops, time_to_train, line, position_in_screen, description):
        db = SessionLocal()
        new_training = Training(name, amount_of_ops, time_to_train, line, position_in_screen, description)
        db.add(new_training)
        db.commit()
        db.close()

        for operator_id in self.operators:
            new_training.assign_operator(operator_id)
        self.trainings[new_training.id] = new_training

    def delete_training(self, training_id):
        if training_id not in self.trainings:
            return False
        db = SessionLocal()
        db.query(Training).filter_by(id=training_id).delete()
        db.query(Training_Operator_training_Status).filter_by(training_id=training_id).delete()
        db.commit()
        db.close()

        del self.trainings[training_id]
        return True

    def update_training_status(self, training_id, operator_id, new_status):
        if training_id not in self.trainings or operator_id not in self.operators:
            return False

        db = SessionLocal()
        row = db.query(Training_Operator_training_Status).filter_by(training_id=training_id, operator_id=operator_id).first()

        if row:
            row.status = new_status
            row.timestamp = datetime.utcnow()
        else:
            new_row = Training_Operator_training_Status(
                training_id=training_id,
                operator_id=operator_id,
                status=new_status,
                timestamp=datetime.utcnow()
            )
            db.add(new_row)

        db.commit()
        db.close()

        # Update operator status in memory
        self.trainings[training_id].operator_statuses[operator_id] = new_status
        return True

    def toggle_training_priority(self, training_id):
        if training_id not in self.trainings:
            return False
        self.trainings[training_id].priority_flag = not self.trainings[training_id].priority_flag

    def get_trainings(self):
        return list(self.trainings.values())

    def get_operators(self):
        return list(self.operators.values())
