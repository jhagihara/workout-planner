# Workout Recommendation System Plan

## 1. Project Overview
Build an end-to-end ML-driven system that:
- Tracks user workouts (exercises, sets, reps, load, rest, RPE, notes)
- Generates adaptive workout splits and routines
- Provides actionable suggestions to improve lift performance and balance muscle groups
- Demonstrates full-stack ML engineering with data ingestion, analytics, ML modeling, and deployment

## 2. Goals & Scope
### In-Scope
- Logging workouts per user, including sets, reps, load, RPE, rest, and notes
- Database storage (PostgreSQL)
- Feature engineering: volume, progression, workload balance, fatigue metrics
- ML models:
  - Predict next-session performance
  - Plateau risk classification
  - Adaptive split recommendations
- Recommendation engine combining rules + ML
- Optional dashboard or API for visualization and interaction


## 3. Technology Stack
- **Backend:** Python (Flask)
- **Database:** PostgreSQL
- **ML/Analytics:** Pandas, NumPy, scikit-learn, PyTorch, Tensorflow
- **Frontend (optional):** React
- **Version control:** Git

## 4. Project Modules
1. **Data Ingestion**
   - Logging workouts via scripts or API
   - Validation and storage in PostgreSQL

2. **Analytics / Feature Engineering**
   - Compute derived metrics: volume, intensity, progression, fatigue index
   - Rolling averages and muscle-group coverage calculations

3. **ML Core**
   - Regression: predict next-session performance
   - Classification: plateau risk
   - Optional clustering or collaborative filtering for routine personalization

4. **Recommendation Engine**
   - Rule-based heuristics: weak muscle groups, recovery, session balance
   - ML-based ranking: combine predicted readiness and user history
   - Output: adaptive workout split

5. **UI/API Layer**
   - Endpoints: `/log`, `/progress`, `/recommend`
   - Optional dashboard with visualizations of trends and suggestions

## 5. Data Schema (PostgreSQL)
- `users`: `user_id`, `username`, `start_date`
- `exercises`: `exercise_id`, `name`, `muscle_group`
- `sessions`: `session_id`, `user_id`, `session_date`
- `sets`: `set_id`, `session_id`, `exercise_id`, `reps`, `weight`, `RPE`, `rest_seconds`
- Derived metrics stored in analytics layer or separate table

## 6. Milestones / Roadmap
1. Design schema and create PostgreSQL database
2. Implement data ingestion scripts or API
3. Populate initial dataset (manual + synthetic)
4. Feature engineering and analytics pipeline
5. Baseline ML models (regression and classification)
6. Rule-based recommendation engine
7. Integrate ML-based adaptive split generator
8. Feedback loop: update models with new user data
9. Optional: frontend/dashboard for visualization
10. Testing and evaluation of predictions and recommendations

## 7. Dependencies & Tools
- Python >=3.9
- PostgreSQL
- Pandas, NumPy, scikit-learn, PyTorch/LightGBM
- FastAPI or Flask
- Streamlit (optional)
- Matplotlib/Plotly for visualization
- Docker (optional for deployment)

## 8. Notes / Considerations
- Start with single-user prototype; scale to multi-user with collaborative filtering later
- Use synthetic data to bootstrap ML training before real user logs
- Track metrics to validate ML predictions and recommendation effectiveness
- Keep modular architecture to allow swapping models, DB, or API independently
