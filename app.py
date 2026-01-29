from flask import Flask, jsonify, render_template, request
from training_board import TrainingBoard
from db_setup import SessionLocal
from models.training_obj import Training
from models.operator_obj import Operator
from models.training_statuses import TrainingStatus, Training_Operator_training_Status  # Assuming you have a TrainingStatus model
from datetime import datetime

app = Flask(__name__)
board = TrainingBoard()
db = SessionLocal()


@app.route("/")
def show_trainings():
    # Use in-memory board (already synced with DB)
    trainings = board.trainings.values()
    operators_dict = board.operators

    return render_template(
        "training.html",
        trainings=trainings,
        operators_dict=operators_dict
    )

@app.route("/update_statuses", methods=["POST"])
def update_statuses():
    """
    Receive updates from frontend and persist to DB.
    Expected payload:
    {
        "trainings": {
            "45": {"16": "trained", "17": "not_trained"}
        }
    }
    """
    data = request.json
    #print(data["trainings"][45])  # Debugging line
    for training_id, operator_dict in data.get("trainings", {}).items():
        for operator_id, status in operator_dict.items():
            # Update DB
            db_status = (
                db.query(Training_Operator_training_Status)
                .filter_by(training_id=int(training_id), operator_id=int(operator_id))
                .first()
            )
            if db_status:
                db_status.status = status
            else:
                # If no record exists, create it
                
                new_status = Training_Operator_training_Status(
                    training_id=str(training_id),
                    operator_id=int(operator_id),
                    status=status,
                    date_assigned=datetime.utcnow()  # or datetime.now() depending on your preference
)
                db.add(new_status)

            # Also update in-memory board
            training = board.trainings.get(training_id)
            if training:
                training.update_operator_status(operator_id, status)

    db.commit()  # ✅ Persist all changes
    board.load_from_db()

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
