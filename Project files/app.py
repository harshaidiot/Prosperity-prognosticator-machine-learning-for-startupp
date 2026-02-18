from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load model from templates directory
model_path = os.path.join(os.path.dirname(__file__), 'templates', 'random_forest_model.pkl')
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request must be JSON with prediction fields', 'success': False}), 400

        # Helpers for parsing and validation
        def get_float(key, required=True, minimum=None):
            if key not in data:
                if required:
                    raise ValueError(f"Missing required field: {key}")
                return 0.0
            try:
                val = float(data.get(key))
            except Exception:
                raise ValueError(f"Field '{key}' must be a number")
            if minimum is not None and val < minimum:
                raise ValueError(f"Field '{key}' must be >= {minimum}")
            return val

        def get_int(key, required=True, minimum=None):
            if key not in data:
                if required:
                    raise ValueError(f"Missing required field: {key}")
                return 0
            try:
                val = int(data.get(key))
            except Exception:
                raise ValueError(f"Field '{key}' must be an integer")
            if minimum is not None and val < minimum:
                raise ValueError(f"Field '{key}' must be >= {minimum}")
            return val

        # Numerical fields
        latitude = get_float('latitude', required=False)
        longitude = get_float('longitude', required=False)
        age_first_funding = get_float('age_first_funding', required=True, minimum=0)
        age_last_funding = get_float('age_last_funding', required=True, minimum=0)
        age_first_milestone = get_float('age_first_milestone', required=True, minimum=0)
        age_last_milestone = get_float('age_last_milestone', required=True, minimum=0)
        relationships = get_int('relationships', required=True, minimum=0)
        funding_rounds = get_int('funding_rounds', required=True, minimum=0)
        total_funding = get_float('total_funding', required=True, minimum=0)
        milestones = get_int('milestones', required=True, minimum=0)
        avg_participants = get_float('avg_participants', required=True, minimum=0)

        # Categorical and flags
        state = data.get('state', 'other')
        category = data.get('category', 'other')

        def get_flag(key):
            v = data.get(key, 0)
            try:
                return int(bool(v))
            except Exception:
                raise ValueError(f"Field '{key}' must be 0/1 or boolean")

        has_vc = get_flag('has_vc')
        has_angel = get_flag('has_angel')
        has_roundA = get_flag('has_roundA')
        has_roundB = get_flag('has_roundB')
        has_roundC = get_flag('has_roundC')
        has_roundD = get_flag('has_roundD')
        is_top500 = get_flag('is_top500')

        # One-hot for state (as used when model was trained)
        is_CA = 1 if state == 'CA' else 0
        is_NY = 1 if state == 'NY' else 0
        is_MA = 1 if state == 'MA' else 0
        is_TX = 1 if state == 'TX' else 0
        is_otherstate = 1 if state == 'other' else 0

        # Build input vector in exact order the model expects
        input_data = [
            latitude,
            longitude,
            age_first_funding,
            age_last_funding,
            age_first_milestone,
            age_last_milestone,
            relationships,
            funding_rounds,
            total_funding,
            milestones,
            is_CA,
            is_NY,
            is_MA,
            is_TX,
            is_otherstate,
            has_vc,
            has_angel,
            has_roundA,
            has_roundB,
            has_roundC,
            has_roundD,
            avg_participants,
            is_top500
        ]

        # Make prediction using loaded model
        try:
            prediction = model.predict([input_data])[0]
        except ValueError as ve:
            return jsonify({'error': f'Model prediction error: {ve}', 'success': False}), 500
        except Exception as e:
            return jsonify({'error': f'Unexpected prediction error: {e}', 'success': False}), 500

        # Map prediction to meaningful output
        result = 'Acquired' if prediction == 1 else 'Closed'
        return jsonify({'prediction': result, 'success': True})

    except ValueError as e:
        return jsonify({'error': str(e), 'success': False}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {e}', 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True)
