import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Create backend directory if not exists
if not os.path.exists('backend'):
    os.makedirs('backend')

# Load dataset
print("Loading dataset...")
csv_path = os.path.join(os.path.dirname(__file__), '../archive/data.csv')
df = pd.read_csv(csv_path, sep=';')

# Data Cleaning: Strip whitespace from column names if any
df.columns = df.columns.str.strip()

# Handle Target mapping
# Dropout -> 2 (High Risk), Enrolled -> 1 (Medium Risk), Graduate -> 0 (Low Risk)
target_map = {'Dropout': 2, 'Enrolled': 1, 'Graduate': 0}
df['RiskLevel'] = df['Target'].map(target_map)

# Feature Selection (Selecting relevant features for student performance)
# Based on user request categories:
# attendance: Daytime/evening attendance
# marks: Curricular units 2nd sem (grade)
# assignments: Curricular units 2nd sem (approved)
# financial: Debtor, Scholarship holder, Tuition fees up to date
# age: Age at enrollment (extra)
features = [
    'Daytime/evening attendance',
    'Curricular units 2nd sem (grade)',
    'Curricular units 2nd sem (approved)',
    'Debtor',
    'Scholarship holder',
    'Tuition fees up to date',
    'Age at enrollment'
]

X = df[features]
y = df['RiskLevel']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42)
}

# Train and compare
best_model = None
best_accuracy = 0
best_model_name = ""

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"{name} Accuracy: {acc:.4f}")
    
    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model
        best_model_name = name

print(f"\nBest Model: {best_model_name} with Accuracy: {best_accuracy:.4f}")

# Save the best model
joblib.dump(best_model, 'model.pkl')
# Save feature names for reference in API
joblib.dump(features, 'features.pkl')

print("Model saved as model.pkl")
