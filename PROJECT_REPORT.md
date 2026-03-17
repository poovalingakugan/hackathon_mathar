# Project Report: EduPredict AI - Student Dropout Prediction System

This document provides a comprehensive overview of the student dropout prediction system, documented from inception to final deployment.

---

## 1. Project Objective
The goal was to build an AI-powered system that predicts the risk of a student dropping out based on academic, behavioral, and financial data. The system doesn't just give a prediction—it explains **why** a risk exists and provides actionable **suggestions** for intervention.

## 2. Technology Stack

### Frontend (User Interface)
- **HTML5 & Vanilla CSS3**: Used for a high-performance, custom-branded interface without the weight of large frameworks.
- **JavaScript (ES6+)**: Handles form logic, cinematic transitions, and real-time API communication.
- **Chart.js**: Utilized for the interactive Global Overview dashboard to visualize student risk distribution.
- **FontAwesome & Google Fonts (Inter)**: Integrated for a modern, premium aesthetic.

### Backend (API & Logic)
- **Python & Flask**: Chosen for its lightweight structure and seamless integration with data science libraries.
- **Flask-CORS**: Enabled to allow secure communication between the frontend and backend.
- **Joblib**: Used for efficient model persistence (saving and loading the trained ML model).

### Machine Learning
- **Pandas & NumPy**: For data manipulation and pre-processing.
- **Scikit-Learn**: The core library used for training and evaluating the prediction model.

---

## 3. The Machine Learning Model

### Model Choice: Logistic Regression
We selected **Logistic Regression** for this project because:
1. **Interpretability**: Unlike "black-box" models, Logistic Regression allows us to see how each feature (like attendance or marks) influences the result, which is critical for **Explainable AI**.
2. **Efficiency**: It is fast to train and very efficient for real-time predictions on small-to-medium datasets.
3. **Probability Scoring**: It naturally provides risk percentages (0-100%), which we used to drive our "Risk Probability" displays.

### Data Processing Steps
1. **Dataset**: A student database containing features like attendance, marks, assignments, and financial status.
2. **Encoding**: Categorical data (like shift or status) was converted to numerical format using Label Encoding.
3. **Splitting**: The data was split into Training (80%) and Testing (20%) sets to ensure accuracy.
4. **Accuracy**: The model achieved a reliable accuracy of ~73% on the test set.

---

## 4. Key Cinematic Features

### Cinematic "Analyzer" Experience
Rather than an instant result, we implemented a **5-second processing screen** with:
- A real-time **0-100% loading counter**.
- A dynamic **progress bar**.
- High-end **animations** (Pulse & Glitch loaders).
- *This builds trust with the user, showing that the "AI" is performing a deep analysis of multiple factors.*

### Multi-Factor Explainable AI
The backend runs a complex logical layer after the model predicts:
- **Reasoning**: Collects multiple risk factors simultaneously (e.g., Low Attendance + Failing Grades).
- **Actionable Suggestions**: Provides specific, bulleted points for intervention (e.g., "Schedule Mandatory Parent-Teacher Meeting").

---

## 5. Development Workflow (From Scratch)
1. **Initial Setup**: Defined project structure and initialized Git.
2. **ML Training**: Wrote `train_model.py` to process the Kaggle dataset and export `model.pkl`.
3. **API Development**: Created `app.py` (Flask) to serve predictions and dashboard stats.
4. **UI Design**: Built `index.html` and `style.css` with a premium "Glassmorphism" design.
5. **Logic Refinement**: Implemented the cinematic 5s delay and multi-line results in `script.js`.
6. **Documentation**: Created README, Requirements, and this Project Report.
7. **Deployment**: Pushed the finalized code to the GitHub repository.

---
**Build by EduPredict AI | 2026**
