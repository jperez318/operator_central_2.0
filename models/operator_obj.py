from sqlalchemy import Column, String, Integer
from db_setup import Base
import uuid

class Operator(Base):
    __tablename__ = "operators"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    op_month_points = Column(Integer, default=0)
    op_month_points_last_month = Column(Integer, default=0)

    def reset_month_points(self):
        #Reset this operator's monthly points to 0
        self.op_month_points_last_month = self.op_month_points
        self.op_month_points = 0

    def to_String(self):
        return f"<Operator(id={self.id}, name={self.name}, points={self.op_month_points}, points_last_month={self.op_month_points_last_month})>"