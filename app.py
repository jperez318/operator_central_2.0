from flask import Flask, render_template
from training_board import TrainingBoard

app = Flask(__name__)
board = TrainingBoard()

@app.route("/")
@app.route("/")
def show_training():
    board = TrainingBoard()
    trainings = board.get_trainings()

    if not trainings:
        return "No trainings found"

    training = trainings[0]
    operators = board.get_operators()

    # build a dict to easily look up operator by ID
    operators_dict = {op.id: op for op in operators}

    # debug print (optional)
    print("Operator statuses for training:", training.operator_statuses)

    return render_template(
        "training.html",
        training=training,
        operators_dict=operators_dict
    )


if __name__ == "__main__":
    app.run(debug=True)
