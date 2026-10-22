# MarketMind — E-commerce Customer Intelligence

MarketMind is a full-stack machine-learning portfolio project that analyzes synthetic e-commerce customer data and provides customer-level predictions and insights through an interactive dashboard.

## Features

- **Churn prediction:** Estimate whether a customer may churn.
- **Spending prediction:** Predict customer spending using a trained regression model.
- **Customer insights:** Generate customer-level analytical insights.
- **Customer segmentation:** Group customers using K-Means clustering.
- **Anomaly detection:** Identify unusual customer profiles using Isolation Forest.
- **Similar customers:** Find customers with similar feature profiles using KNN.
- **Customer management:** Save and list customer records through a REST API.
- **Interactive dashboard:** Explore the features through a React and TypeScript interface.

## Tech Stack

**Frontend:** React, TypeScript, Vite, Recharts

**Backend:** Python, FastAPI, Pydantic, SQLAlchemy

**Database:** SQLite

**Machine Learning:** pandas, NumPy, scikit-learn, XGBoost, joblib

## Architecture

The React dashboard sends HTTP requests to the FastAPI backend. The backend validates inputs, loads trained model artifacts, generates predictions or analytical results, and uses SQLite for customer records.

```text
React + TypeScript Dashboard
            |
            v
       FastAPI REST API
        /      |      \
       v       v       v
    ML Models CSV Data SQLite
```

## Project Structure

```text
ecommerce-ml/
├── data/          # Customer dataset
├── frontend/      # React + TypeScript application
├── images/        # Visualizations
├── models/        # Trained models and scalers
├── reports/       # Generated analysis reports
├── src/
│   ├── database/  # Database connection and models
│   ├── main.py    # FastAPI application
│   └── train_*.py # Model training scripts
├── tests/         # Automated API tests
└── requirements.txt
```

## Run Locally

### 1. Install Python dependencies

Activate your existing Conda environment, or create a compatible Python environment, then run from the project root:

```bash
python -m pip install -r requirements.txt
```

### 2. Initialize the database

```bash
python -m src.database.init_db
```

### 3. Start the backend

```bash
uvicorn src.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

Interactive API documentation: `http://127.0.0.1:8000/docs`

### 4. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite normally serves the dashboard at `http://localhost:5173`.

For local development, configure `VITE_API_BASE_URL` in your local frontend environment file as:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Keep local `.env` files private; do not commit them.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/customers` | Save a customer |
| GET | `/customers` | List customer records |
| POST | `/predict/churn` | Predict churn |
| POST | `/predict/spending` | Predict spending |
| POST | `/customers/insights` | Generate customer insights |
| POST | `/customers/segment` | Assign a customer segment |
| POST | `/customers/anomalies` | Detect anomalies |
| POST | `/customers/similar` | Find similar customers |

See `/docs` for request schemas and interactive API testing.

## Testing and Quality Checks

Run backend tests from the project root:

```bash
python -m pytest -q
```

Check Python dependencies:

```bash
python -m pip check
```

Build the frontend:

```bash
cd frontend
npm run build
```

Run frontend linting:

```bash
npm run lint
```

At the time of writing, the project owner has verified **23 passing backend tests**, a clean dependency check, and successful frontend build and lint checks.

## Machine-Learning Notes

The repository contains training scripts and saved artifacts for approaches including logistic regression, linear regression, decision trees, random forests, gradient boosting, SVM, XGBoost, K-Means, KNN, and Isolation Forest.

The presence of a saved model does not necessarily mean every model is used by a current API endpoint. Refer to the implementation and training scripts for exact behavior.

The dataset is synthetic. Results demonstrate an end-to-end ML workflow, not validated performance on real customers. Model evaluation on representative held-out data is necessary before making claims about real-world effectiveness.

## Future Improvements

- Document evaluation metrics and training procedures for each model.
- Expand edge-case and data-quality tests.
- Add database migrations as the schema evolves.
- Improve reproducibility and model versioning.
- Optimize frontend bundle size if performance measurements justify it.
- Validate model performance on representative real-world data.

## Portfolio Summary

MarketMind demonstrates a full-stack ML workflow spanning data preparation, model training, model artifacts, API development, database integration, frontend visualization, and automated testing. It is a local learning and portfolio project, not a validated production decision system.

