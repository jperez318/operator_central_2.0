from enum import Enum

class TrainingStatus(Enum):
    NOT_TRAINED = 0
    TRAINED = 1
    RAN_IN_WORKSHOP = 2
    SHADOWED = 3
    CAN_TRAIN = 4