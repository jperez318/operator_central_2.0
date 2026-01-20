import uuid

class Operator:
    def __init__(self, name, id=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.op_month_points = 0

    def reset_month_points(self):
        self.op_month_points = 0