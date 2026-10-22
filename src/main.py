import joblib

import pandas as pd

from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from pydantic import BaseModel, Field

# Create FastAPI application

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from src.database.connection import SessionLocal
from src.database.models import CustomerDB

class Customer(BaseModel):
    age: int = Field(..., ge=18, le=100)
    membership_years: int = Field(..., ge=0, le=100)
    total_orders: int = Field(..., ge=0)
    average_order_value: float = Field(..., gt=0)
    days_since_last_purchase: int = Field(..., ge=0)
    total_spending: float = Field(..., ge=0)


class ChurnRequest(BaseModel):

    age: int = Field(..., ge=18, le=100)

    membership_years: int = Field(..., ge=0, le=100)

    total_orders: int = Field(..., ge=0)

    average_order_value: float = Field(..., gt=0)

    days_since_last_purchase: int = Field(..., ge=0)

    total_spending: float = Field(..., ge=0)

class SpendingRequest(BaseModel):

    age: int = Field(..., ge=18, le=100)

    membership_years: int = Field(..., ge=0, le=100)

    total_orders: int = Field(..., ge=0)

    average_order_value: float = Field(..., gt=0)

    days_since_last_purchase: int = Field(..., ge=0)

app = FastAPI(

    title="E-commerce ML API",

    description="API for our machine learning project",

    version="1.0.0",

)

@app.exception_handler(Exception)
async def unexpected_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected server error occurred."
        },
    )


LOCAL_FRONTEND_ORIGINS = [

    "http://localhost:5173",

    "http://127.0.0.1:5173",

]

app.add_middleware(

    CORSMiddleware,

    allow_origins=LOCAL_FRONTEND_ORIGINS,

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],

)

BASE_DIR = Path(__file__).resolve().parent.parent

# Load customer records for similar-customer recommendations

customers_df = pd.read_csv(BASE_DIR / "data" / "customers.csv")

model_path = BASE_DIR / "models"/"logistic_regression.pkl"

churn_model = joblib.load(model_path)

linear_model_path = BASE_DIR / "models" / "linear_regression.pkl"

linear_model = joblib.load(linear_model_path)

kmeans_model_path = BASE_DIR / "models" / "kmeans.pkl"

kmeans_model = joblib.load(kmeans_model_path)

kmeans_scaler_path = BASE_DIR / "models" / "kmeans_scaler.pkl"

kmeans_scaler = joblib.load(kmeans_scaler_path)

isolation_forest_path = BASE_DIR / "models" / "isolation_forest.pkl"

isolation_forest_model = joblib.load(isolation_forest_path)

# Load the KNN model for finding similar customers

knn_model_path = BASE_DIR / "models" / "knn.pkl"

knn_model = joblib.load(knn_model_path)

# Load the scaler used when training the KNN model

knn_scaler_path = BASE_DIR / "models" / "knn_scaler.pkl"

knn_scaler = joblib.load(knn_scaler_path)

# Create the first endpoint

@app.get("/")

def home():

    return{

        "message": "E-commerce ML API is running!",

        "status": "success",

    }

@app.get("/health")

def health_check():

    return{

        "status":"healthy",

        "message":"E-commerce ML backend is Working"

    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/customers")
def create_customer(
    customer: Customer,
    db: Session = Depends(get_db),
):
    try:
        db_customer = CustomerDB(
            age=customer.age,
            membership_years=customer.membership_years,
            total_orders=customer.total_orders,
            average_order_value=customer.average_order_value,
            days_since_last_purchase=customer.days_since_last_purchase,
            total_spending=customer.total_spending,
        )

        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        return {
            "message": "Customer saved successfully!",
            "customer": {
                "id": db_customer.id,
                "age": db_customer.age,
                "membership_years": db_customer.membership_years,
                "total_orders": db_customer.total_orders,
                "average_order_value": db_customer.average_order_value,
                "days_since_last_purchase": db_customer.days_since_last_purchase,
                "total_spending": db_customer.total_spending,
            },
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save customer due to a database error.",
        )

@app.post("/predict/churn")

def predict_churn(customer: ChurnRequest):

    features = pd.DataFrame([{

    "age": customer.age,

    "membership_years": customer.membership_years,

    "total_orders": customer.total_orders,

    "average_order_value": customer.average_order_value,

    "days_since_last_purchase": customer.days_since_last_purchase,

    "total_spending": customer.total_spending,

}])

    prediction = churn_model.predict(features)[0]

    probability = churn_model.predict_proba(features)[0][1]

    return {

        "churn_prediction": int(prediction),

        "churn_probability": round(float(probability), 4),

        "message": "Customer may churn" if prediction == 1 else "Customer may stay"

    }

@app.post("/predict/spending")

def predict_spending(customer: SpendingRequest):

    features = pd.DataFrame([{

    "age": customer.age,

    "membership_years": customer.membership_years,

    "total_orders": customer.total_orders,

    "average_order_value": customer.average_order_value,

    "days_since_last_purchase": customer.days_since_last_purchase,

}])

    predicted_spending=linear_model.predict(features)[0]

    return{

        "predicted_total_spending":round(float(predicted_spending),2),

        "message":"Customer spending prediction generated successfully!"

        }

class CustomerInsightsRequest(BaseModel):

    age: int = Field(..., ge=18, le=100)

    membership_years: int = Field(..., ge=0, le=100)

    total_orders: int = Field(..., ge=0)

    average_order_value: float = Field(..., gt=0)

    days_since_last_purchase: int = Field(..., ge=0)

    total_spending: float = Field(..., ge=0)

@app.post("/customers/insights")

def customer_insights(customer: CustomerInsightsRequest):

    days = customer.days_since_last_purchase

    # Rule-based engagement insight

    if days >= 90:

        risk_level = "high"

        recommendation = "Consider a customer retention campaign."

    elif days >= 30:

        risk_level = "medium"

        recommendation = "Consider sending a personalized offer."

    else:

        risk_level = "low"

        recommendation = "Continue regular customer engagement."

    # ML-based churn prediction

    features = pd.DataFrame([{

    "age": customer.age,

    "membership_years": customer.membership_years,

    "total_orders": customer.total_orders,

    "average_order_value": customer.average_order_value,

    "days_since_last_purchase": customer.days_since_last_purchase,

    "total_spending": customer.total_spending,

}])

    churn_prediction = int(churn_model.predict(features)[0])

    churn_probability = float(churn_model.predict_proba(features)[0][1])

    churn_status = "Likely to churn" if churn_prediction == 1 else "Likely to stay"

    return {

        "days_since_last_purchase": days,

        "engagement_risk": risk_level,

        "recommendation": recommendation,

        "churn_prediction": churn_prediction,

        "churn_probability": round(churn_probability, 4),

        "churn_status": churn_status,

    }

class SegmentationRequest(BaseModel):

    total_orders: int = Field(..., ge=0)

    average_order_value: float = Field(..., gt=0)

    days_since_last_purchase: int = Field(..., ge=0)

    total_spending: float = Field(..., ge=0)

class AnomalyRequest(BaseModel):

    age: int = Field(..., ge=18, le=100)

    membership_years: int = Field(..., ge=0, le=100)

    total_orders: int = Field(..., ge=0)

    average_order_value: float = Field(..., gt=0)

    days_since_last_purchase: int = Field(..., ge=0)

    total_spending: float = Field(..., ge=0)

@app.post("/customers/segment")

def segment_customer(customer: SegmentationRequest):

    features = pd.DataFrame([{
        "total_orders": customer.total_orders,
        "average_order_value": customer.average_order_value,
        "days_since_last_purchase": customer.days_since_last_purchase,
        "total_spending": customer.total_spending,
    }])

    scaled_features = kmeans_scaler.transform(features)

    segment = int(kmeans_model.predict(scaled_features)[0])

    return {

        "customer_segment": segment,

        "message": "Customer segment assigned successfully!"

    }

@app.post("/customers/anomalies")

def detect_customer_anomaly(customer: AnomalyRequest):

    features = pd.DataFrame([{
        "age": customer.age,
        "membership_years": customer.membership_years,
        "total_orders": customer.total_orders,
        "average_order_value": customer.average_order_value,
        "days_since_last_purchase": customer.days_since_last_purchase,
        "total_spending": customer.total_spending,
    }])

    prediction = int(isolation_forest_model.predict(features)[0])

    return {

        "is_anomaly": prediction == -1,

        "anomaly_prediction": prediction,

        "message": (

            "Unusual customer pattern detected. Review this record."

            if prediction == -1

            else "No unusual pattern detected."

        )

    }

class SimilarCustomersRequest(BaseModel):

    age: int = Field(..., ge=18, le=100)

    membership_years: int = Field(..., ge=0, le=100)

    total_orders: int = Field(..., ge=0)

    average_order_value: float = Field(..., gt=0)

    days_since_last_purchase: int = Field(..., ge=0)

    total_spending: float = Field(..., ge=0)

@app.post("/customers/similar")

def find_similar_customers(customer: SimilarCustomersRequest):

    # 1. Prepare the customer's features in training order

    features = pd.DataFrame([{
        "age": customer.age,
        "membership_years": customer.membership_years,
        "total_orders": customer.total_orders,
        "average_order_value": customer.average_order_value,
        "days_since_last_purchase": customer.days_since_last_purchase,
        "total_spending": customer.total_spending,
    }])

    # 2. Scale the features using the original training scaler

    scaled_features = knn_scaler.transform(features)

    # 3. Find the five nearest customers

    distances, indices = knn_model.kneighbors(

        scaled_features,

        n_neighbors=5

    )

    # 4. Retrieve their profiles from the dataset

    similar_customers = []

    for distance, index in zip(distances[0], indices[0]):

        row = customers_df.iloc[int(index)]

        similar_customers.append({

            "customer_id": int(row["customer_id"]),

            "age": int(row["age"]),

            "total_orders": int(row["total_orders"]),

            "average_order_value": float(row["average_order_value"]),

            "days_since_last_purchase": int(row["days_since_last_purchase"]),

            "total_spending": float(row["total_spending"]),

            "similarity_distance": round(float(distance), 4),

        })

    return {

        "message": "Similar customers found successfully!",

        "count": len(similar_customers),

        "similar_customers": similar_customers,

    }

@app.get("/customers")
def get_customers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    customers = (
        db.query(CustomerDB)
        .order_by(CustomerDB.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    total = db.query(CustomerDB).count()

    return {
        "total": total,
        "count": len(customers),
        "skip": skip,
        "limit": limit,
        "customers": [
            {
                "id": customer.id,
                "age": customer.age,
                "membership_years": customer.membership_years,
                "total_orders": customer.total_orders,
                "average_order_value": customer.average_order_value,
                "days_since_last_purchase": customer.days_since_last_purchase,
                "total_spending": customer.total_spending,
            }
            for customer in customers
        ],
    }

