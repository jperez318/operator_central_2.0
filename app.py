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
    for training_id, operator_dict in data.get("trainings", {}).items():
        for operator_id, status in operator_dict.items():
            db_status = (
                db.query(Training_Operator_training_Status)
                .filter_by(training_id=int(training_id), operator_id=int(operator_id))
                .first()
            )
            if db_status:
                db_status.status = status
            else:
                new_status = Training_Operator_training_Status(
                    training_id=int(training_id),
                    operator_id=int(operator_id),
                    status=status,
                    date_assigned=datetime.utcnow()
                )
                db.add(new_status)

            # Also update in-memory board
            training = board.trainings.get(training_id)
            if training:
                training.update_operator_status(operator_id, status)

    db.commit()
    board.load_from_db()

    return jsonify({"success": True})

@app.route("/operators", methods=["POST"])
def add_operator():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name required"}), 400

    db = SessionLocal()
    try:
        operator = Operator(name=name)
        db.add(operator)
        db.flush()
        trainings = db.query(Training).all()
        for training in trainings:
            status = Training_Operator_training_Status(
                training_id=training.id,
                operator_id=operator.id,
                status="not_trained",
                date_assigned=datetime.utcnow()
            )
            db.add(status)
        db.commit()
        return jsonify({
            "id": operator.id,
            "name": operator.name
        })

    finally:
        db.close()
        board.load_from_db()

@app.route("/operators/<int:operator_id>", methods=["DELETE"])
def delete_operator(operator_id):
    db = SessionLocal()
    try:
        db.query(Training_Operator_training_Status)\
          .filter_by(operator_id=operator_id)\
          .delete()

        db.query(Operator)\
          .filter_by(id=operator_id)\
          .delete()

        db.commit()
        return jsonify({"success": True})

    finally:
        db.close()
        board.load_from_db()


if __name__ == "__main__":
    app.run(debug=True)
