
from fastapi.testclient import TestClient

from src.main import app
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch
from fastapi import HTTPException
client = TestClient(app, raise_server_exceptions=False)


def test_unexpected_error_returns_safe_response():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from unittest.mock import patch
    from src.main import unexpected_error_handler

    test_app = FastAPI()
    test_app.add_exception_handler(
        Exception,
        unexpected_error_handler,
    )

    @test_app.get("/test-error")
    def trigger_error():
        raise RuntimeError("Sensitive internal details")

    test_client = TestClient(
        test_app,
        raise_server_exceptions=False,
    )

    response = test_client.get("/test-error")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An unexpected server error occurred."
    }
    assert "Sensitive internal details" not in response.text

def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_customers():
    response = client.get("/customers")

    assert response.status_code == 200

    data = response.json()
    assert "count" in data
    assert "customers" in data
    assert isinstance(data["customers"], list)
    assert data["count"] == len(data["customers"])

    if data["count"] > 0:
        customer = data["customers"][0]
        assert "id" in customer
        assert "age" in customer
        assert "total_spending" in customer


def test_get_customers_pagination():
    response = client.get("/customers?skip=0&limit=2")

    assert response.status_code == 200

    data = response.json()
    assert data["skip"] == 0
    assert data["limit"] == 2
    assert data["count"] <= 2
    assert data["count"] == len(data["customers"])


def test_get_customers_rejects_negative_skip():
    response = client.get("/customers?skip=-1&limit=2")

    assert response.status_code == 422


def test_get_customers_rejects_zero_limit():
    response = client.get("/customers?skip=0&limit=0")

    assert response.status_code == 422


def test_get_customers_rejects_limit_over_100():
    response = client.get("/customers?skip=0&limit=101")

    assert response.status_code == 422


def test_churn_prediction():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/predict/churn", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "churn_prediction" in data
    assert "churn_probability" in data
    assert "message" in data

    assert data["churn_prediction"] in [0, 1]
    assert 0 <= data["churn_probability"] <= 1


def test_churn_rejects_invalid_age():
    payload = {
        "age": 10,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/predict/churn", json=payload)

    assert response.status_code == 422

def test_spending_prediction():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
    }

    response = client.post("/predict/spending", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "predicted_total_spending" in data
    assert isinstance(data["predicted_total_spending"], (int, float))
    assert data["predicted_total_spending"] >= 0



def test_customer_insights():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/customers/insights", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "engagement_risk" in data
    assert "recommendation" in data
    assert "churn_prediction" in data
    assert "churn_probability" in data
    assert "churn_status" in data


def test_customer_segmentation():
    payload = {
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/customers/segment", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "customer_segment" in data
    assert isinstance(data["customer_segment"], int)
    assert "message" in data

def test_anomaly_detection():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/customers/anomalies", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "is_anomaly" in data
    assert isinstance(data["is_anomaly"], bool)
    assert data["anomaly_prediction"] in [-1, 1]
    assert "message" in data

def test_similar_customers():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/customers/similar", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "similar_customers" in data
    assert isinstance(data["similar_customers"], list)
    assert len(data["similar_customers"]) == 5

def test_churn_rejects_missing_required_field():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        # total_spending is intentionally missing
    }

    response = client.post("/predict/churn", json=payload)

    assert response.status_code == 422


def test_churn_rejects_negative_spending():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": -100.0,
    }

    response = client.post("/predict/churn", json=payload)

    assert response.status_code == 422


def test_churn_accepts_minimum_valid_age():
    payload = {
        "age": 18,
        "membership_years": 0,
        "total_orders": 0,
        "average_order_value": 100.0,
        "days_since_last_purchase": 0,
        "total_spending": 0.0,
    }

    response = client.post("/predict/churn", json=payload)

    assert response.status_code == 200
    assert response.json()["churn_prediction"] in [0, 1]

def test_churn_accepts_maximum_valid_age():
    payload = {
        "age": 100,
        "membership_years": 100,
        "total_orders": 0,
        "average_order_value": 100.0,
        "days_since_last_purchase": 0,
        "total_spending": 0.0,
    }

    response = client.post("/predict/churn", json=payload)

    assert response.status_code == 200
    assert response.json()["churn_prediction"] in [0, 1]

def test_churn_rejects_age_above_maximum():
    payload = {
        "age": 101,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/predict/churn", json=payload)

    assert response.status_code == 422

def test_spending_rejects_zero_average_order_value():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 0.0,
        "days_since_last_purchase": 45,
    }

    response = client.post("/predict/spending", json=payload)

    assert response.status_code == 422

def test_create_customer_rejects_invalid_age():
    payload = {
        "age": 10,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/customers", json=payload)

    assert response.status_code == 422

def test_create_customer_accepts_valid_data():
    payload = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    response = client.post("/customers", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Customer saved successfully!"
    assert data["customer"]["id"] is not None
    assert data["customer"]["age"] == 30
    assert data["customer"]["membership_years"] == 2
    assert data["customer"]["total_orders"] == 10
    assert data["customer"]["average_order_value"] == 500.0
    assert data["customer"]["days_since_last_purchase"] == 45
    assert data["customer"]["total_spending"] == 5000.0

def test_create_customer_handles_database_error():
    from unittest.mock import patch

    customer_data = {
        "age": 30,
        "membership_years": 2,
        "total_orders": 10,
        "average_order_value": 500.0,
        "days_since_last_purchase": 45,
        "total_spending": 5000.0,
    }

    with patch("src.main.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        db.commit.side_effect = SQLAlchemyError("Simulated database failure")

        response = client.post("/customers", json=customer_data)

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Unable to save customer due to a database error."
    )
    db.rollback.assert_called_once()
    db.close.assert_called_once()
