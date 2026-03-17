from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load the model and features
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
features_path = os.path.join(os.path.dirname(__file__), 'features.pkl')

if os.path.exists(model_path) and os.path.exists(features_path):
    model = joblib.load(model_path)
    features_list = joblib.load(features_path)
else:
    model = None
    features_list = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not trained yet"}), 500
    
    data = request.json
    
    # Map incoming JSON to our feature list
    # attendance (1/0), marks (0-20), assignments (0-20), discipline (not used but mapped), financial (0/1)
    # Mapping logic:
    # attendance -> Daytime/evening attendance
    # marks -> Curricular units 2nd sem (grade)
    # assignments -> Curricular units 2nd sem (approved)
    # financial -> Debtor (if financial is 1, debtor is 1)
    # We also need defaults for Scholarship holder, Tuition fees up to date, Age at enrollment
    
    try:
        attendance_pct = float(data.get('attendance', 100))
        
        input_data = {
            # Map percentage to binary for the model: >70% -> Daytime (1), <=70% -> Evening (0)
            'Daytime/evening attendance': 1 if attendance_pct > 70 else 0,
            'Curricular units 2nd sem (grade)': float(data.get('marks', 12)),
            'Curricular units 2nd sem (approved)': int(data.get('assignments', 6)),
            'Debtor': int(data.get('financial', 0)),
            'Scholarship holder': 0, # Default
            'Tuition fees up to date': 1 if int(data.get('financial', 0)) == 0 else 0,
            'Age at enrollment': 20 # Default
        }
        
        # Convert to DataFrame for model prediction
        input_df = pd.DataFrame([input_data])[features_list]
        
        # Prediction
        probabilities = model.predict_proba(input_df)[0]
        
        # Calculate Risk Percentage
        high_prob = probabilities[2]
        med_prob = probabilities[1]
        
        risk_percentage = (high_prob * 100) + (med_prob * 50)
        
        # Adjust for Attendance: Every 1% below 100 adds 0.5% risk penalty
        if attendance_pct < 100:
            risk_percentage += (100 - attendance_pct) * 0.8 # More aggressive penalty
            
        # Adjust for discipline: Each case adds 10% to risk (max 100)
        discipline_cases = int(data.get('discipline', 0))
        risk_percentage += (discipline_cases * 10)
        risk_percentage = min(100, round(risk_percentage, 2))

        # Re-evaluate risk level based on calculated percentage
        if risk_percentage > 70:
            risk_level = "High Risk"
        elif risk_percentage > 35:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"
        
        # Explainable AI: Logic-based multi-factor explanation
        reasons = []
        suggestions = []
        
        if attendance_pct < 85:
            reasons.append(f"Low Attendance: Student has only {attendance_pct}% attendance, which is below the safe threshold of 85%.")
            suggestions.append("Immediate transport or health support check is recommended.")
            if attendance_pct < 70:
                reasons.append("Critical Alert: Attendance is below 70%, indicating high risk of total disengagement.")
                suggestions.append("Schedule a mandatory parent-teacher meeting to discuss attendance barriers.")

        if discipline_cases > 0:
            reasons.append(f"Behavioral Issues: student has {discipline_cases} discipline cases recorded on file.")
            suggestions.append("Enroll student in proactive behavioral counseling and mentorship programs.")
            if discipline_cases > 2:
                reasons.append("High Discipline Severity: Multiple cases suggest recurring behavioral patterns.")
                suggestions.append("Immediate intervention by the student welfare office is required.")

        if input_data['Curricular units 2nd sem (grade)'] < 12:
            reasons.append(f"Academic Struggle: Marks ({input_data['Curricular units 2nd sem (grade)']}) are currently below the target level.")
            suggestions.append("Provide access to the academic tutoring center for specialized core subject help.")
            if input_data['Curricular units 2nd sem (grade)'] < 8:
                reasons.append("Failing Grades: Current academic performance is at a failing level.")
                suggestions.append("Reduce elective load or provide intensive remedial classes.")

        if input_data['Curricular units 2nd sem (approved)'] < 10:
            reasons.append("Low Assignment Completion: Many curricular units remain unapproved/incomplete.")
            suggestions.append("Assign a student coach to help with time management and assignment planning.")

        if input_data['Debtor'] == 1:
            reasons.append("Financial Stress: Outstanding tuition fees and personal debt detected.")
            suggestions.append("Guide the student to the bursar's office for scholarship applications or installment plans.")

        if not reasons:
            reasons.append("No significant risk factors identified at this time.")
            suggestions.append("Maintain current performance and encourage extra-curricular participation.")

        # Join with bullet points for clean UI display
        final_reason = "\n• " + "\n• ".join(reasons)
        final_suggestion = "\n• " + "\n• ".join(suggestions)

        return jsonify({
            "risk_level": risk_level,
            "risk_percentage": risk_percentage,
            "reason": final_reason,
            "suggestion": final_suggestion
        })

    except Exception as e:
        print(f"ERROR in /predict: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/stats', methods=['GET'])
def stats():
    # Return some mock stats for the dashboard if real data analysis is too slow
    # Total students: 4426
    # Dropout (High): 1421
    # Enrolled (Medium): 794
    # Graduate (Low): 2211
    return jsonify({
        "total_students": 4426,
        "high_risk": 1421,
        "medium_risk": 794,
        "low_risk": 2211
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
