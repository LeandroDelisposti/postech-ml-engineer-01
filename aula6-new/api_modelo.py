from logging import config
import os
import logging
import datetime
import jwt
from functools import wraps

from flask import Flask, request, jsonify
import joblib
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from predictions import Prediction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_modelo")

JWT_SECRET = "mothafuckingsecret02s"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 120000

DB_URL = "sqlite:///predictions.db"
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Prediction.metadata.bind = engine

# Create the database tables (in production use migrations  )
Prediction.metadata.create_all(engine)

model = joblib.load("modelo_iris.pkl")
logger.info("Model loaded successfully")

app = Flask(__name__)
predictions_cache = {}

TEST_USERNAME = "admin"
TEST_PASSWORD = "secret"

def create_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            # check expiration
            if data['exp'] < datetime.datetime.utcnow().timestamp():
                return jsonify({'message': 'Token has expired!'}), 401

            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401
    if auth.username == TEST_USERNAME and auth.password == TEST_PASSWORD:
        token = create_token(auth.username)
        return jsonify({'token': token})
    return jsonify({'message': 'Could not verify'}), 401

@app.route('/predict', methods=['POST'])
@token_required
def predict():
    """Make a prediction using the pre-trained model.
    Expects a JSON payload with sepal_length, sepal_width, petal_length, petal_width.
    Caches predictions to optimize performance.
    Body (JSON):
    {
        "sepal_length": float,
        "sepal_width": float,
        "petal_length": float,
        "petal_width": float
    }
    """
    data = request.get_json()
    sepal_length = data.get("sepal_length")
    sepal_width = data.get("sepal_width")
    petal_length = data.get("petal_length")
    petal_width = data.get("petal_width")

    input_tuple = (sepal_length, sepal_width, petal_length, petal_width)

    if input_tuple in predictions_cache:
        predicted_class = predictions_cache[input_tuple]
        logger.info("Cache hit for input: %s", input_tuple)
    else:
        input_array = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        prediction = model.predict(input_array)
        predicted_class = int(prediction[0])
        predictions_cache[input_tuple] = predicted_class
        logger.info("Cache miss for input: %s. Prediction made: %s", input_tuple, predicted_class)

    # Save prediction to the database
    session = SessionLocal()
    prediction_record = Prediction(
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
        predicted_class=predicted_class
    )
    session.add(prediction_record)
    session.commit()
    session.close()

    return jsonify({
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
        "predicted_class": predicted_class
    })

@app.route("/predictions", methods=["GET"])
@token_required
def get_predictions():
    """Retrieve all past predictions from the database.
    Returns a list of prediction records.
    Body (JSON):
    [
        {
            "sepal_length": float,
            "sepal_width": float,
            "petal_length": float,
            "petal_width": float,
            "predicted_class": string,
            "created_at": datetime
        },
        ...
    """
    limit = request.args.get("limit", default=100, type=int)
    offset = request.args.get("offset", default=0, type=int)
    session = SessionLocal()
    predictions = session.query(Prediction).order_by(Prediction.created_at.desc()).limit(limit).offset(offset).all()
    session.close()
    return jsonify([{
        "sepal_length": float(p.sepal_length),
        "sepal_width": float(p.sepal_width),
        "petal_length": float(p.petal_length),
        "petal_width": float(p.petal_width),
        "predicted_class": int(p.predicted_class),
        "created_at": p.created_at.isoformat() if p.created_at is not None else None
    } for p in predictions])

@app.route("/predictions/<int:id>", methods=["DELETE"])
@token_required
def delete_predictions(id):
    """Delete a specific prediction from the database by ID."""
    session = SessionLocal()
    session.query(Prediction).filter(Prediction.id == id).delete()
    session.commit()
    session.close()
    return jsonify({"message": f"Prediction with ID {id} deleted"}), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True)