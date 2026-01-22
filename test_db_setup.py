from db_setup import SessionLocal
from models.operator_obj import Operator
from models.training_obj import Training
from training_board import TrainingBoard

def test_read_operators_and_trainings():
    print("🚀 Script started")

    # Create a DB session
    db = SessionLocal()
    print("📦 DB session created")

    try:
        # Query all operators
        print("🔍 Querying operators table")
        operators = db.query(Operator).all()
        print(f"✅ Found {len(operators)} operators:")
        for op in operators:
            print(f" - {op.id}: {op.name}, Points: {op.op_month_points}")

    except Exception as e:
        print("❌ Error querying operators:", e)

    try:
        # Query all trainings
        print("🔍 Querying triainings table")
        trainings = db.query(Training).all()
        print(f"✅ Found {len(trainings)} trainings:")
        for training in trainings:
            print(f" - {training.id}: {training.name}, Amount of Ops: {training.amount_of_ops_needed}, Time to Train: {training.time_to_train}, Line: {training.line}, Priority Flag: {training.priority_flag}, Position in Screen: {training.position_in_screen}")
    except Exception as e:
        print("❌ Error querying operators:", e)

    finally:
        db.close()
        print("🔒 DB session closed")



def test_training_board():
    print("🚀 Initializing TrainingBoard from DB")
    board = TrainingBoard()  # loads operators, trainings, and operator_statuses

    print(f"✅ Loaded {len(board.get_operators())} operators")
    for op in board.get_operators():
        print(f" - {op.id}: {op.name}")

    print(f"✅ Loaded {len(board.get_trainings())} trainings")
    for training in board.get_trainings():
        print(f" - {training.id}: {training.name}")
        print("   Operator statuses:")
        for op_id, status in training.operator_statuses.items():
            print(f"     {op_id}: {status}")
        break

    # Pick first training and first operator to test update
    training_id = board.get_trainings()[0].id
    operator_id = board.get_operators()[0].id
    
    print(f"\n🚀 Updating status for training {training_id}, operator {operator_id} to 'TRAINED'")
    board.update_training_status(training_id, operator_id, "TRAINED")

    # Verify in-memory update
    updated_status = board.trainings[training_id].operator_statuses[operator_id]
    print(f"✅ Updated in-memory status: {updated_status}")

    # Optional: reload board to verify DB persistence
    print("\n🔁 Reloading TrainingBoard to check DB persistence")
    board = TrainingBoard()
    persisted_status = board.trainings[training_id].operator_statuses[operator_id]
    print(f"✅ Status persisted in DB: {persisted_status}")
    
    
if __name__ == "__main__":
    #test_read_operators_and_trainings()
    test_training_board()
