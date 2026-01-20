from training_board import TrainingBoard

board = TrainingBoard()
board.add_operator("Alice")
board.add_operator("Bob")
assert len(board.operators) == 2